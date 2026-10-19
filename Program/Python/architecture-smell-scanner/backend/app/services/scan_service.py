import os
import tempfile
import shutil
import asyncio
from datetime import datetime
from typing import Optional
import httpx

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Scan, Project, ArchitectureSmell, ScanStatus, SeverityLevel, ProgrammingLanguage
from app.scanner.analyzer import CodeAnalyzer
from app.core.config import settings


class ScanService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def start_scan(self, scan_id: int):
        """Start the scan process"""
        # Update scan status to running
        scan_result = await self.db.execute(select(Scan).where(Scan.id == scan_id))
        scan = scan_result.scalar_one_or_none()
        
        if not scan:
            return
        
        scan.status = ScanStatus.RUNNING
        scan.started_at = datetime.utcnow()
        await self.db.flush()
        
        try:
            # Get project
            project_result = await self.db.execute(select(Project).where(Project.id == scan.project_id))
            project = project_result.scalar_one_or_none()
            
            if not project:
                raise Exception("Project not found")
            
            # Get code directory
            code_dir = await self._get_code_directory(project)
            
            if not code_dir or not os.path.exists(code_dir):
                raise Exception("Code directory not found")
            
            # Analyze code
            analyzer = CodeAnalyzer()
            smells = await analyzer.analyze_directory(code_dir)
            
            # Save smells to database
            for smell_data in smells:
                smell = ArchitectureSmell(
                    scan_id=scan_id,
                    smell_type=smell_data["smell_type"],
                    severity=smell_data["severity"],
                    file_path=smell_data["file_path"],
                    line_number=smell_data.get("line_number"),
                    class_name=smell_data.get("class_name"),
                    method_name=smell_data.get("method_name"),
                    description=smell_data["description"],
                    suggestion=smell_data.get("suggestion"),
                    code_snippet=smell_data.get("code_snippet"),
                    language=smell_data["language"]
                )
                self.db.add(smell)
            
            await self.db.flush()
            
            # Calculate health score
            health_score = self._calculate_health_score(smells)
            
            # Update scan with results
            scan.status = ScanStatus.COMPLETED
            scan.completed_at = datetime.utcnow()
            scan.health_score = health_score
            scan.total_smells = len(smells)
            scan.critical_count = len([s for s in smells if s["severity"] == SeverityLevel.CRITICAL])
            scan.high_count = len([s for s in smells if s["severity"] == SeverityLevel.HIGH])
            scan.medium_count = len([s for s in smells if s["severity"] == SeverityLevel.MEDIUM])
            scan.low_count = len([s for s in smells if s["severity"] == SeverityLevel.LOW])
            
            await self.db.commit()
            
        except Exception as e:
            scan.status = ScanStatus.FAILED
            scan.error_message = str(e)
            scan.completed_at = datetime.utcnow()
            await self.db.commit()
    
    async def _get_code_directory(self, project: Project) -> Optional[str]:
        """Get the code directory for a project"""
        if project.code_snapshot_path and os.path.exists(project.code_snapshot_path):
            # If it's a zip file, extract it
            if project.code_snapshot_path.endswith('.zip'):
                extract_dir = project.code_snapshot_path.replace('.zip', '')
                if not os.path.exists(extract_dir):
                    shutil.unpack_archive(project.code_snapshot_path, extract_dir)
                return extract_dir
            return project.code_snapshot_path
        
        if project.git_url:
            # Clone the repository
            temp_dir = tempfile.mkdtemp()
            try:
                # For git URLs, use git clone
                # In production, use asyncio.to_thread for git operations
                result = await asyncio.create_subprocess_exec(
                    'git', 'clone', '--depth', '1', project.git_url, temp_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await result.communicate()
                
                if result.returncode == 0:
                    return temp_dir
            except Exception:
                pass
        
        return None
    
    def _calculate_health_score(self, smells: list) -> int:
        """Calculate health score based on smells"""
        score = 100
        
        for smell in smells:
            if smell["severity"] == SeverityLevel.CRITICAL:
                score -= 15
            elif smell["severity"] == SeverityLevel.HIGH:
                score -= 8
            elif smell["severity"] == SeverityLevel.MEDIUM:
                score -= 3
            elif smell["severity"] == SeverityLevel.LOW:
                score -= 1
        
        return max(0, score)