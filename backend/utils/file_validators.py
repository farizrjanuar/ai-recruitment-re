"""
File Validation Utilities

This module provides utilities for validating uploaded files including
size validation, format validation, content validation, and secure filename generation.
"""

import os
import re
import uuid
from typing import Tuple, Optional
from werkzeug.utils import secure_filename


class FileValidator:
    """
    Handles file validation for CV uploads.
    
    Validates:
    - File size (max 5MB)
    - File format (PDF, DOCX, TXT only)
    - File content (minimum text length)
    - Generates secure filenames
    """
    
    # Maximum file size: 5MB
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    
    # Minimum text length after extraction (characters)
    MIN_TEXT_LENGTH = 50
    
    def __init__(self):
        """Initialize the FileValidator."""
        pass
    
    def validate_file_size(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a file does not exceed the maximum size limit.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if file size is acceptable, False otherwise
            - error_message: None if valid, error description if invalid
        """
        try:
            if not os.path.exists(file_path):
                return False, "File does not exist"
            
            file_size = os.path.getsize(file_path)
            
            if file_size == 0:
                return False, "File is empty"
            
            if file_size > self.MAX_FILE_SIZE:
                size_mb = file_size / (1024 * 1024)
                max_mb = self.MAX_FILE_SIZE / (1024 * 1024)
                return False, f"File size ({size_mb:.2f}MB) exceeds maximum allowed size ({max_mb}MB)"
            
            return True, None
            
        except Exception as e:
            return False, f"Error checking file size: {str(e)}"
    
    def validate_file_format(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that a file has an allowed extension.
        
        Args:
            filename: Name of the file to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if file format is acceptable, False otherwise
            - error_message: None if valid, error description if invalid
        """
        if not filename:
            return False, "Filename is empty"
        
        # Extract file extension
        if '.' not in filename:
            return False, "File has no extension"
        
        extension = filename.rsplit('.', 1)[1].lower()
        
        if extension not in self.ALLOWED_EXTENSIONS:
            allowed = ', '.join(sorted(self.ALLOWED_EXTENSIONS))
            return False, f"File format '.{extension}' is not supported. Allowed formats: {allowed}"
        
        return True, None
    
    def get_file_extension(self, filename: str) -> Optional[str]:
        """
        Extract and return the file extension.
        
        Args:
            filename: Name of the file
            
        Returns:
            File extension in lowercase (without dot), or None if no extension
        """
        if not filename or '.' not in filename:
            return None
        
        return filename.rsplit('.', 1)[1].lower()
    
    def validate_file_content(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that extracted text meets minimum length requirements.
        
        Args:
            text: Extracted text content to validate
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if content is acceptable, False otherwise
            - error_message: None if valid, error description if invalid
        """
        if not text:
            return False, "No text content found in file"
        
        # Remove whitespace for length check
        text_stripped = text.strip()
        
        if len(text_stripped) < self.MIN_TEXT_LENGTH:
            return False, f"File content is too short ({len(text_stripped)} characters). Minimum required: {self.MIN_TEXT_LENGTH} characters"
        
        return True, None
    
    def generate_secure_filename(self, original_filename: str, prefix: str = "cv") -> str:
        """
        Generate a secure, unique filename while preserving the file extension.
        
        Args:
            original_filename: Original filename from upload
            prefix: Prefix for the generated filename (default: "cv")
            
        Returns:
            Secure filename with format: prefix_uuid.extension
        """
        # Get the file extension
        extension = self.get_file_extension(original_filename)
        
        if not extension:
            extension = "txt"  # Default extension if none found
        
        # Generate unique identifier
        unique_id = uuid.uuid4().hex
        
        # Create secure filename
        secure_name = f"{prefix}_{unique_id}.{extension}"
        
        return secure_name
    
    def validate_filename_characters(self, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that filename contains only safe characters.
        
        Args:
            filename: Filename to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is empty"
        
        # Check for path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False, "Filename contains invalid path characters"
        
        # Check for null bytes
        if '\x00' in filename:
            return False, "Filename contains null bytes"
        
        return True, None
    
    def validate_file(self, file_path: str, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Perform complete file validation (size and format).
        
        Args:
            file_path: Path to the file
            filename: Original filename
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if all validations pass, False otherwise
            - error_message: None if valid, error description if invalid
        """
        # Validate filename characters
        is_valid, error = self.validate_filename_characters(filename)
        if not is_valid:
            return False, error
        
        # Validate file format
        is_valid, error = self.validate_file_format(filename)
        if not is_valid:
            return False, error
        
        # Validate file size
        is_valid, error = self.validate_file_size(file_path)
        if not is_valid:
            return False, error
        
        return True, None


# Convenience function for quick validation
def validate_uploaded_file(file_path: str, filename: str) -> Tuple[bool, Optional[str]]:
    """
    Convenience function to validate an uploaded file.
    
    Args:
        file_path: Path to the uploaded file
        filename: Original filename
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = FileValidator()
    return validator.validate_file(file_path, filename)
