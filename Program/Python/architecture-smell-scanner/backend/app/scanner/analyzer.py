import os
import ast
from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import networkx as nx

from app.models import SeverityLevel, ProgrammingLanguage


@dataclass
class Smell:
    smell_type: str
    severity: SeverityLevel
    file_path: str
    line_number: Optional[int]
    class_name: Optional[str]
    method_name: Optional[str]
    description: str
    suggestion: Optional[str]
    code_snippet: Optional[str]
    language: ProgrammingLanguage


class PythonAnalyzer:
    """Analyzer for Python code"""
    
    # Thresholds from requirements
    MAX_CLASS_LINES = 500
    MAX_METHODS_PER_CLASS = 30
    
    def __init__(self):
        self.smells: List[Dict] = []
        self.import_graph = nx.DiGraph()
        self.file_to_module: Dict[str, str] = {}
        self.class_info: Dict[str, Dict] = {}
    
    def analyze_file(self, file_path: str) -> List[Dict]:
        """Analyze a single Python file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                content = f.read()
                tree = ast.parse(content, filename=file_path)
                self._analyze_imports(file_path, tree)
                self._analyze_classes(file_path, tree, content)
                self._analyze_functions(file_path, tree, content)
            except SyntaxError:
                pass  # Skip files with syntax errors
        
        return self.smells
    
    def _analyze_imports(self, file_path: str, tree: ast.AST):
        """Extract import information for dependency analysis"""
        module_name = self._get_module_name(file_path)
        self.file_to_module[file_path] = module_name
        
        if module_name not in self.import_graph:
            self.import_graph.add_node(module_name)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported = alias.asname if alias.asname else alias.name
                    self.import_graph.add_edge(module_name, imported)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.import_graph.add_edge(module_name, node.module)
    
    def _analyze_classes(self, file_path: str, tree: ast.AST, content: str):
        """Analyze classes for God Class and Feature Envy"""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_info = self._get_class_info(node)
                self.class_info[f"{file_path}:{node.name}"] = class_info
                
                # God Class detection
                if class_info['lines'] > self.MAX_CLASS_LINES:
                    self.smells.append(self._create_smell(
                        smell_type="GodClass",
                        severity=SeverityLevel.HIGH,
                        file_path=file_path,
                        line_number=node.lineno,
                        class_name=node.name,
                        description=f"Class '{node.name}' has {class_info['lines']} lines, exceeding the {self.MAX_CLASS_LINES} line threshold",
                        suggestion="Consider splitting this class into smaller, more focused classes using principles like Single Responsibility Principle."
                    ))
                
                if class_info['method_count'] > self.MAX_METHODS_PER_CLASS:
                    self.smells.append(self._create_smell(
                        smell_type="GodClass",
                        severity=SeverityLevel.HIGH,
                        file_path=file_path,
                        line_number=node.lineno,
                        class_name=node.name,
                        description=f"Class '{node.name}' has {class_info['method_count']} methods, exceeding the {self.MAX_METHODS_PER_CLASS} method threshold",
                        suggestion="Consider extracting related methods into separate classes or modules."
                    ))
                
                # Feature Envy detection
                self._detect_feature_envy(node, file_path, content)
    
    def _detect_feature_envy(self, class_node: ast.ClassDef, file_path: str, content: str):
        """Detect Feature Envy - when a class is too interested in another class's data"""
        # Count method calls to self vs external objects
        external_calls = 0
        self_calls = 0
        
        for node in ast.walk(class_node):
            if isinstance(node, ast.Attribute):
                if isinstance(node.value, ast.Name):
                    if node.value.id == 'self':
                        self_calls += 1
                    else:
                        external_calls += 1
        
        # If external calls significantly exceed self calls, it might be Feature Envy
        if self_calls > 0 and external_calls > self_calls * 2:
            self.smells.append(self._create_smell(
                smell_type="FeatureEnvy",
                severity=SeverityLevel.MEDIUM,
                file_path=file_path,
                line_number=class_node.lineno,
                class_name=class_node.name,
                description=f"Class '{class_node.name}' seems more interested in another class's data than its own",
                suggestion="Consider moving methods that heavily use another class's data to that class, or use the 'Move Method' refactoring technique."
            ))
    
    def _analyze_functions(self, file_path: str, tree: ast.AST, content: str):
        """Analyze functions for Shotgun Surgery"""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node)
        
        # Shotgun Surgery: multiple functions modify the same set of variables
        # Simplified detection: look for functions with similar parameter patterns
        param_sets = {}
        for func in functions:
            params = tuple(sorted([arg.arg for arg in func.args.args]))
            if params:
                if params not in param_sets:
                    param_sets[params] = []
                param_sets[params].append((func.name, func.lineno))
        
        # If multiple functions modify similar data, might be Shotgun Surgery
        for params, funcs in param_sets.items():
            if len(funcs) >= 3:
                for name, lineno in funcs[:1]:  # Report first occurrence
                    self.smells.append(self._create_smell(
                        smell_type="ShotgunSurgery",
                        severity=SeverityLevel.MEDIUM,
                        file_path=file_path,
                        line_number=lineno,
                        method_name=name,
                        description=f"Multiple functions ({len(funcs)}) operate on similar data patterns, indicating potential Shotgun Surgery",
                        suggestion="Consider consolidating these related operations into a single class or module to reduce scattered changes."
                    ))
    
    def _get_class_info(self, node: ast.ClassDef) -> Dict:
        """Get comprehensive class information"""
        method_count = 0
        line_count = node.end_lineno - node.lineno + 1 if hasattr(node, 'end_lineno') and node.end_lineno else 0
        
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_count += 1
        
        return {
            'lines': line_count,
            'method_count': method_count,
            'node': node
        }
    
    def detect_circular_dependencies(self) -> List[Dict]:
        """Detect circular dependencies between modules"""
        try:
            # Find strongly connected components (cycles)
            sccs = list(nx.strongly_connected_components(self.import_graph))
            
            for scc in sccs:
                if len(scc) > 1:  # Only report actual cycles
                    # Get the cycle path
                    for node1 in scc:
                        for node2 in scc:
                            if node1 != node2:
                                try:
                                    path = nx.shortest_path(self.import_graph, node1, node2)
                                    # Simplified: just report the cycle exists
                                    return [{
                                        "smell_type": "CircularDependency",
                                        "severity": SeverityLevel.CRITICAL,
                                        "file_path": node1,
                                        "line_number": None,
                                        "class_name": None,
                                        "method_name": None,
                                        "description": f"Circular dependency detected: {' -> '.join(path)} creates a cycle",
                                        "suggestion": "Break the circular dependency by introducing an interface or extracting shared code into a third module.",
                                        "code_snippet": None,
                                        "language": ProgrammingLanguage.PYTHON
                                    }]
                                except nx.NetworkXNoPath:
                                    continue
        except Exception:
            pass
        
        return []
    
    def _get_module_name(self, file_path: str) -> str:
        """Convert file path to module name"""
        rel_path = os.path.relpath(file_path)
        module_name = rel_path.replace(os.sep, '.').replace('/', '.')[:-3]  # Remove .py
        return module_name
    
    def _create_smell(self, **kwargs) -> Dict:
        """Create a smell dictionary"""
        return {
            "smell_type": kwargs.get("smell_type"),
            "severity": kwargs.get("severity"),
            "file_path": kwargs.get("file_path"),
            "line_number": kwargs.get("line_number"),
            "class_name": kwargs.get("class_name"),
            "method_name": kwargs.get("method_name"),
            "description": kwargs.get("description"),
            "suggestion": kwargs.get("suggestion"),
            "code_snippet": kwargs.get("code_snippet"),
            "language": ProgrammingLanguage.PYTHON
        }


class DuplicateCodeDetector:
    """Detect duplicate code across the codebase"""
    
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
        self.smells: List[Dict] = []
    
    def find_duplicates(self, file_paths: List[str]) -> List[Dict]:
        """Find duplicate code across multiple files"""
        code_blocks = []
        
        # Extract code blocks (functions and methods)
        for file_path in file_paths:
            if file_path.endswith('.py'):
                blocks = self._extract_python_blocks(file_path)
                code_blocks.extend(blocks)
        
        # Compare blocks for similarity
        duplicates = self._find_similar_blocks(code_blocks)
        
        return duplicates
    
    def _extract_python_blocks(self, file_path: str) -> List[Tuple[str, str, int]]:
        """Extract code blocks (functions/classes) from a Python file"""
        blocks = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                content = f.read()
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                            lines = content.split('\n')[node.lineno-1:node.end_lineno]
                            code = '\n'.join(lines)
                            if len(code.strip()) > 10:  # Ignore very short blocks
                                blocks.append((node.name, code, node.lineno))
            except SyntaxError:
                pass
        
        return blocks
    
    def _find_similar_blocks(self, blocks: List[Tuple[str, str, int]]) -> List[Dict]:
        """Find blocks with similarity above threshold"""
        duplicates = []
        
        for i, (name1, code1, line1) in enumerate(blocks):
            for j, (name2, code2, line2) in enumerate(blocks[i+1:], i+1):
                similarity = self._calculate_similarity(code1, code2)
                if similarity >= self.similarity_threshold:
                    duplicates.append({
                        "smell_type": "DuplicateCode",
                        "severity": SeverityLevel.LOW,
                        "file_path": f"Block 1: {name1}, Block 2: {name2}",
                        "line_number": min(line1, line2),
                        "class_name": None,
                        "method_name": None,
                        "description": f"Duplicate code detected with {similarity:.0%} similarity",
                        "suggestion": "Extract the duplicated code into a shared function or utility module.",
                        "code_snippet": f"Similar code found in {name1} and {name2}",
                        "language": ProgrammingLanguage.PYTHON
                    })
        
        return duplicates
    
    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity between two code blocks using simple token comparison"""
        # Normalize code (remove whitespace, comments)
        normalized1 = self._normalize_code(code1)
        normalized2 = self._normalize_code(code2)
        
        if normalized1 == normalized2:
            return 1.0
        
        # Simple Jaccard similarity based on tokens
        tokens1 = set(normalized1.split())
        tokens2 = set(normalized2.split())
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = len(tokens1 & tokens2)
        union = len(tokens1 | tokens2)
        
        return intersection / union if union > 0 else 0.0
    
    def _normalize_code(self, code: str) -> str:
        """Normalize code by removing comments and whitespace"""
        lines = []
        for line in code.split('\n'):
            # Remove inline comments
            if '#' in line:
                line = line[:line.index('#')]
            line = line.strip()
            if line:
                lines.append(line)
        return ' '.join(lines)


class CodeAnalyzer:
    """Main code analyzer that combines all analysis"""
    
    def __init__(self):
        self.smells: List[Dict] = []
    
    async def analyze_directory(self, directory: str) -> List[Dict]:
        """Analyze all code files in a directory"""
        self.smells = []
        
        # Find all supported file types
        python_files = list(Path(directory).rglob("*.py"))
        java_files = list(Path(directory).rglob("*.java"))
        js_files = list(Path(directory).rglob("*.js"))
        ts_files = list(Path(directory).rglob("*.ts"))
        tsx_files = list(Path(directory).rglob("*.tsx"))
        
        # Analyze Python files
        python_analyzer = PythonAnalyzer()
        for py_file in python_files:
            # Skip virtual environments and test files
            if 'venv' in str(py_file) or 'env' in str(py_file) or '__pycache__' in str(py_file):
                continue
            python_analyzer.analyze_file(str(py_file))
        
        self.smells.extend(python_analyzer.smells)
        
        # Check for circular dependencies
        circular_deps = python_analyzer.detect_circular_dependencies()
        self.smells.extend(circular_deps)
        
        # Find duplicate code
        duplicate_detector = DuplicateCodeDetector()
        duplicates = duplicate_detector.find_duplicates([str(f) for f in python_files])
        self.smells.extend(duplicates)
        
        # Analyze Java files (simplified)
        self._analyze_java_files(java_files)
        
        # Analyze JS/TS files (simplified)
        self._analyze_js_ts_files(js_files + ts_files + tsx_files)
        
        return self.smells
    
    def _analyze_java_files(self, java_files: List[Path]):
        """Analyze Java files for architecture smells"""
        # Simplified Java analysis - in production would use JavaParser
        for java_file in java_files:
            if 'venv' in str(java_file) or 'node_modules' in str(java_file):
                continue
            
            with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Count lines per class
                class_lines = content.count('public class')
                if class_lines > 0:
                    lines = content.count('\n')
                    if lines > 500:
                        self.smells.append({
                            "smell_type": "GodClass",
                            "severity": SeverityLevel.HIGH,
                            "file_path": str(java_file),
                            "line_number": 1,
                            "class_name": None,
                            "method_name": None,
                            "description": f"Large Java file with {lines} lines detected",
                            "suggestion": "Consider splitting into smaller classes following Single Responsibility Principle.",
                            "code_snippet": content[:200] + "..." if len(content) > 200 else content,
                            "language": ProgrammingLanguage.JAVA
                        })
    
    def _analyze_js_ts_files(self, files: List[Path]):
        """Analyze JavaScript/TypeScript files for architecture smells"""
        for file in files:
            if 'node_modules' in str(file):
                continue
            
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Check for large files
                lines = content.count('\n')
                if lines > 500:
                    self.smells.append({
                        "smell_type": "GodClass",
                        "severity": SeverityLevel.MEDIUM,
                        "file_path": str(file),
                        "line_number": 1,
                        "class_name": None,
                        "method_name": None,
                        "description": f"Large JavaScript/TypeScript file with {lines} lines detected",
                        "suggestion": "Consider splitting into smaller modules following the single responsibility principle.",
                        "code_snippet": content[:200] + "..." if len(content) > 200 else content,
                        "language": ProgrammingLanguage.JAVASCRIPT if file.suffix == '.js' else ProgrammingLanguage.TYPESCRIPT
                    })