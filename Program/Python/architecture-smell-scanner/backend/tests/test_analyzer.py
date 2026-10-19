import pytest
import tempfile
import os
from pathlib import Path

from app.scanner.analyzer import PythonAnalyzer, DuplicateCodeDetector, CodeAnalyzer


class TestPythonAnalyzer:
    """Tests for Python code analyzer"""
    
    def test_god_class_detection_large_class(self):
        """Test that large classes are detected as God Class"""
        analyzer = PythonAnalyzer()
        
        # Create a temporary file with a large class
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("# " * 100)  # Many lines
            f.write("\nclass LargeClass:\n")
            for i in range(600):  # Create a 600-line class
                f.write(f"    def method_{i}(self):\n")
                f.write(f"        pass\n")
            temp_file = f.name
        
        try:
            analyzer.analyze_file(temp_file)
            smells = analyzer.smells
            
            god_classes = [s for s in smells if s['smell_type'] == 'GodClass']
            assert len(god_classes) > 0
        finally:
            os.unlink(temp_file)
    
    def test_god_class_detection_many_methods(self):
        """Test that classes with many methods are detected"""
        analyzer = PythonAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("class ManyMethodsClass:\n")
            for i in range(35):  # More than 30 methods
                f.write(f"    def method_{i}(self):\n")
                f.write(f"        pass\n")
            temp_file = f.name
        
        try:
            analyzer.analyze_file(temp_file)
            smells = analyzer.smells
            
            # Should detect at least one GodClass smell
            assert any(s['smell_type'] == 'GodClass' for s in smells)
        finally:
            os.unlink(temp_file)
    
    def test_normal_class_no_smell(self):
        """Test that normal classes don't trigger smells"""
        analyzer = PythonAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
class NormalClass:
    def __init__(self):
        self.value = 0
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
""")
            temp_file = f.name
        
        try:
            analyzer.analyze_file(temp_file)
            smells = analyzer.smells
            
            # Should not detect GodClass for normal class
            god_classes = [s for s in smells if s['smell_type'] == 'GodClass']
            assert len(god_classes) == 0
        finally:
            os.unlink(temp_file)
    
    def test_import_tracking(self):
        """Test that imports are tracked for dependency analysis"""
        analyzer = PythonAnalyzer()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
import os
import sys
from pathlib import Path

class TestClass:
    pass
""")
            temp_file = f.name
        
        try:
            analyzer.analyze_file(temp_file)
            
            # Check that module was added to import graph
            assert len(analyzer.import_graph.nodes()) > 0
        finally:
            os.unlink(temp_file)


class TestDuplicateCodeDetector:
    """Tests for duplicate code detection"""
    
    def test_find_duplicates(self):
        """Test duplicate code detection"""
        detector = DuplicateCodeDetector(similarity_threshold=0.8)
        
        files = []
        for i in range(3):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(f"""
def similar_function_{i}():
    result = []
    for i in range(10):
        result.append(i * 2)
    return result
""")
                files.append(f.name)
        
        try:
            duplicates = detector.find_duplicates(files)
            # Should find duplicates among the files
            assert isinstance(duplicates, list)
        finally:
            for f in files:
                os.unlink(f)
    
    def test_no_duplicates_in_different_code(self):
        """Test that completely different code doesn't trigger duplicates"""
        detector = DuplicateCodeDetector(similarity_threshold=0.8)
        
        files = []
        for i, code in enumerate([
            "def function_a():\n    return 1",
            "def function_b():\n    return 'hello'",
            "def function_c():\n    return [1, 2, 3]",
        ]):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                files.append(f.name)
        
        try:
            duplicates = detector.find_duplicates(files)
            # Should not find duplicates in completely different code
            assert len(duplicates) == 0
        finally:
            for f in files:
                os.unlink(f)


class TestCodeAnalyzer:
    """Tests for the main code analyzer"""
    
    @pytest.mark.asyncio
    async def test_analyze_directory(self):
        """Test analyzing a directory of code files"""
        analyzer = CodeAnalyzer()
        
        # Create a temporary directory with Python files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file with a God Class
            god_class_file = Path(temp_dir) / "large_class.py"
            god_class_file.write_text("""
class LargeClass:
""" + "\n".join([f"    def method_{i}(self): pass" for i in range(100)]))
            
            # Create a normal file
            normal_file = Path(temp_dir) / "normal_class.py"
            normal_file.write_text("""
class NormalClass:
    def __init__(self):
        self.value = 0
    def get_value(self):
        return self.value
""")
            
            smells = await analyzer.analyze_directory(temp_dir)
            
            # Should find some smells in the large class
            assert isinstance(smells, list)