import React, { useCallback, useState } from 'react';
import { Upload, File, X, Loader2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card, CardContent } from '../ui/Card';

interface FileUploadProps {
    onFileSelect: (file: File | null) => void;
    selectedFile: File | null;
}

export function FileUpload({ onFileSelect, selectedFile }: FileUploadProps) {
    const [isDragging, setIsDragging] = useState(false);

    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setIsDragging(true);
        } else if (e.type === 'dragleave') {
            setIsDragging(false);
        }
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onFileSelect(e.dataTransfer.files[0]);
        }
    }, [onFileSelect]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            onFileSelect(e.target.files[0]);
        }
    };

    return (
        <div className="space-y-4">
            {!selectedFile ? (
                <label
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    className={`
            relative flex flex-col items-center justify-center w-full h-64 rounded-xl border-2 border-dashed transition-all cursor-pointer bg-navy-800
            ${isDragging
                            ? 'border-primary bg-primary/5'
                            : 'border-white/10 hover:border-white/20 hover:bg-navy-700/50'
                        }
          `}
                >
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <div className={`p-4 rounded-full mb-4 ${isDragging ? 'bg-primary/20 text-primary-light' : 'bg-white/5 text-gray-400'}`}>
                            <Upload size={32} />
                        </div>
                        <p className="mb-2 text-sm text-gray-300">
                            <span className="font-semibold text-primary-light">Click to upload</span> or drag and drop
                        </p>
                        <p className="text-xs text-gray-500">PDF, DOCX, or Images (MAX. 10MB)</p>
                    </div>
                    <input type="file" className="hidden" onChange={handleChange} accept=".pdf,.docx,.doc,image/*" />
                </label>
            ) : (
                <Card className="group">
                    <CardContent className="p-4 flex items-center justify-between">
                        <div className="flex items-center gap-4">
                            <div className="p-3 rounded-lg bg-primary/20 text-primary-light">
                                <File size={24} />
                            </div>
                            <div>
                                <p className="font-medium text-white">{selectedFile.name}</p>
                                <p className="text-xs text-gray-400">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                            </div>
                        </div>
                        <Button
                            onClick={() => onFileSelect(null)}
                            variant="ghost"
                            className="text-gray-400 hover:text-white"
                        >
                            <X size={20} />
                        </Button>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
