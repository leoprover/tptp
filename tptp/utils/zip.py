import zipfile
from pathlib import Path


def zip(sourcePath: Path, targetPath: Path):
    with zipfile.ZipFile(targetPath, "w", compression=zipfile.ZIP_DEFLATED) as zipDescriptor:
        if sourcePath.is_file():
            if sourcePath == targetPath:
                raise IOError('The target path is the same as the source path.')
            zipDescriptor.write(str(sourcePath), arcname=sourcePath.name)
            return
        elif sourcePath.is_dir():
            try:
                if targetPath.relative_to(sourcePath):
                    raise IOError(
                        'The target path (zip file) is contained in the directory structure of the source path.')
            except ValueError:
                pass  # not relative
            for file in sourcePath.glob('**/*'):
                print(file.absolute())
                zipDescriptor.write(file.absolute(), arcname=file.relative_to(sourcePath))
            return