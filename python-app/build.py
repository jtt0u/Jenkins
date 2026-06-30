#!/usr/bin/env python3
"""
Build script that generates various artifacts for demonstration
Creates: compiled bytecode, documentation, build reports, and package
"""
import os
import sys
import json
import shutil
from datetime import datetime
import subprocess

def create_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)
    print(f"✓ Created directory: {path}")

def generate_build_info(output_dir):
    """Generate build information JSON file"""
    build_info = {
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'build_number': os.environ.get('BUILD_NUMBER', 'local'),
        'environment': os.environ.get('ENVIRONMENT', 'development'),
        'build_timestamp': datetime.now().isoformat(),
        'build_host': os.environ.get('HOSTNAME', 'unknown'),
        'python_version': sys.version,
        'platform': sys.platform
    }

    output_file = os.path.join(output_dir, 'build-info.json')
    with open(output_file, 'w') as f:
        json.dump(build_info, f, indent=2)

    print(f"✓ Generated build info: {output_file}")
    return build_info

def compile_python_files(output_dir):
    """Compile Python files to bytecode (.pyc)"""
    import py_compile

    files_to_compile = ['app.py']
    compiled_dir = os.path.join(output_dir, 'compiled')
    create_directory(compiled_dir)

    for filename in files_to_compile:
        if os.path.exists(filename):
            output_file = os.path.join(compiled_dir, filename + 'c')
            py_compile.compile(filename, cfile=output_file, doraise=True)
            print(f"✓ Compiled: {filename} -> {output_file}")

    return compiled_dir

def generate_documentation(output_dir):
    """Generate simple documentation"""
    docs_dir = os.path.join(output_dir, 'docs')
    create_directory(docs_dir)

    # Generate API documentation
    api_doc = """# API Documentation

## Jenkins Python Application

**Version:** {version}
**Build:** {build}

### Endpoints

#### GET /
Main application page with UI

#### GET /api/info
Returns application information in JSON format

**Response:**
```json
{{
  "application": "jenkins-python-app",
  "version": "x.x.x",
  "build": "xxx",
  "environment": "xxx"
}}
```

#### GET /api/health
Health check endpoint

**Response:**
```json
{{
  "status": "healthy",
  "version": "x.x.x"
}}
```

#### GET /api/metrics
Application metrics

**Response:**
```json
{{
  "metrics": {{
    "python_version": "x.x.x",
    "platform": "xxx"
  }}
}}
```

## Running the Application

```bash
pip install -r requirements.txt
python app.py
```

## Environment Variables

- `APP_VERSION` - Application version
- `BUILD_NUMBER` - Build number
- `ENVIRONMENT` - Environment name (development/staging/production)
- `PORT` - Server port (default: 5000)
- `DEBUG` - Debug mode (true/false)

Generated: {timestamp}
""".format(
        version=os.environ.get('APP_VERSION', '1.0.0'),
        build=os.environ.get('BUILD_NUMBER', 'local'),
        timestamp=datetime.now().isoformat()
    )

    doc_file = os.path.join(docs_dir, 'API.md')
    with open(doc_file, 'w') as f:
        f.write(api_doc)

    print(f"✓ Generated documentation: {doc_file}")

    # Generate README
    readme = """# Jenkins Python Application

Build artifacts for version {version} (build #{build})

## Contents

- `compiled/` - Compiled Python bytecode
- `docs/` - API documentation
- `build-info.json` - Build metadata
- `requirements.txt` - Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Built on: {timestamp}
""".format(
        version=os.environ.get('APP_VERSION', '1.0.0'),
        build=os.environ.get('BUILD_NUMBER', 'local'),
        timestamp=datetime.now().isoformat()
    )

    readme_file = os.path.join(output_dir, 'README.md')
    with open(readme_file, 'w') as f:
        f.write(readme)

    print(f"✓ Generated README: {readme_file}")

    return docs_dir

def create_package(output_dir, build_info):
    """Create distributable package"""
    package_dir = os.path.join(output_dir, 'package')
    create_directory(package_dir)

    # Copy necessary files
    files_to_package = [
        'app.py',
        'requirements.txt'
    ]

    for filename in files_to_package:
        if os.path.exists(filename):
            shutil.copy(filename, package_dir)
            print(f"✓ Packaged: {filename}")

    # Copy build info
    shutil.copy(
        os.path.join(output_dir, 'build-info.json'),
        package_dir
    )

    # Create version file
    version_file = os.path.join(package_dir, 'VERSION')
    with open(version_file, 'w') as f:
        f.write(f"{build_info['version']}-{build_info['build_number']}\n")

    print(f"✓ Created package in: {package_dir}")

    return package_dir

def generate_build_report(output_dir, build_info):
    """Generate build report"""
    report = """
╔════════════════════════════════════════════════════════════════╗
║           BUILD REPORT - JENKINS PYTHON APPLICATION            ║
╚════════════════════════════════════════════════════════════════╝

Version:        {version}
Build Number:   {build_number}
Environment:    {environment}
Build Time:     {build_timestamp}
Python Version: {python_version}
Platform:       {platform}

════════════════════════════════════════════════════════════════

BUILD ARTIFACTS:
  ✓ Compiled bytecode
  ✓ API documentation
  ✓ Package files
  ✓ Build metadata

LOCATION: {output_dir}

BUILD STATUS: SUCCESS ✓

════════════════════════════════════════════════════════════════
""".format(
        version=build_info['version'],
        build_number=build_info['build_number'],
        environment=build_info['environment'],
        build_timestamp=build_info['build_timestamp'],
        python_version=build_info['python_version'].split('\n')[0],
        platform=build_info['platform'],
        output_dir=output_dir
    )

    report_file = os.path.join(output_dir, 'BUILD-REPORT.txt')
    with open(report_file, 'w') as f:
        f.write(report)

    print(report)
    print(f"✓ Build report saved to: {report_file}")

def main():
    """Main build process"""
    print("=" * 60)
    print("JENKINS PYTHON APPLICATION - BUILD SCRIPT")
    print("=" * 60)

    # Create output directory
    output_dir = 'dist'
    create_directory(output_dir)

    # Generate build artifacts
    build_info = generate_build_info(output_dir)
    compile_python_files(output_dir)
    generate_documentation(output_dir)
    create_package(output_dir, build_info)
    generate_build_report(output_dir, build_info)

    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY ✓")
    print("=" * 60)
    print(f"Artifacts location: {os.path.abspath(output_dir)}")

    return 0

if __name__ == '__main__':
    sys.exit(main())
