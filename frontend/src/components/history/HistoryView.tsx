import React, { useState, useEffect } from 'react';
import { History, Trash2, Eye, Calendar, FileText, CheckCircle, XCircle } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import axios from 'axios';

interface HistoryRecord {
    id: string;
    timestamp: string;
    prompt: string;
    student_level: string;
    department: string;
    submission_format: string;
    use_research: boolean;
    stealth_mode: boolean;
    style_mirrored: boolean;
    email_sent: boolean;
    file_generated: string | null;
    result?: {
        title?: string;
        question?: string;
        summary?: string;
    };
}

export function HistoryView() {
    const [records, setRecords] = useState<HistoryRecord[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedRecord, setSelectedRecord] = useState<HistoryRecord | null>(null);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = async () => {
        setIsLoading(true);
        try {
            const response = await axios.get('http://localhost:8001/api/v1/history');
            if (response.data.success) {
                setRecords(response.data.data);
            }
        } catch (error) {
            console.error('Failed to load history:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const viewDetails = async (recordId: string) => {
        try {
            const response = await axios.get(`http://localhost:8001/api/v1/history/${recordId}`);
            if (response.data.success) {
                setSelectedRecord(response.data.data);
            }
        } catch (error) {
            alert('Failed to load details');
        }
    };

    const deleteRecord = async (recordId: string) => {
        if (!confirm('Are you sure you want to delete this record?')) return;

        try {
            await axios.delete(`http://localhost:8001/api/v1/history/${recordId}`);
            setRecords(records.filter(r => r.id !== recordId));
            if (selectedRecord?.id === recordId) {
                setSelectedRecord(null);
            }
        } catch (error) {
            alert('Failed to delete record');
        }
    };

    const formatDate = (timestamp: string) => {
        return new Date(timestamp).toLocaleString();
    };

    return (
        <div className="space-y-6">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-white">Assignment History</h1>
                <p className="text-gray-400">View and manage past assignment executions</p>
            </div>

            {isLoading ? (
                <Card className="p-12 text-center bg-transparent border-dashed">
                    <p className="text-gray-400">Loading history...</p>
                </Card>
            ) : records.length === 0 ? (
                <Card className="p-12 text-center border-dashed bg-transparent">
                    <History size={48} className="mx-auto mb-4 text-gray-600" />
                    <h3 className="text-xl font-semibold text-white mb-2">No History Yet</h3>
                    <p className="text-gray-400">Your executed assignments will appear here</p>
                </Card>
            ) : (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* List of records */}
                    <div className="lg:col-span-2 space-y-4">
                        {records.map((record) => (
                            <Card key={record.id} className="hover:bg-navy-700/50 transition-colors group">
                                <CardContent className="p-4 flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <Calendar size={14} className="text-gray-500" />
                                            <span className="text-xs text-gray-500 font-medium">{formatDate(record.timestamp)}</span>
                                        </div>
                                        <p className="text-white font-medium mb-3 line-clamp-2">{record.prompt}</p>
                                        <div className="flex flex-wrap gap-2">
                                            <Badge variant="secondary">{record.student_level}</Badge>
                                            <Badge variant="secondary">{record.department}</Badge>
                                            {record.stealth_mode && <Badge variant="destructive">Stealth</Badge>}
                                            {record.style_mirrored && <Badge variant="default">Mirrored</Badge>}
                                            {record.email_sent ? (
                                                <Badge variant="success" className="gap-1"><CheckCircle size={12} /> Sent</Badge>
                                            ) : (
                                                <Badge variant="secondary" className="gap-1 opacity-50"><XCircle size={12} /> Email</Badge>
                                            )}
                                        </div>
                                    </div>
                                    <div className="flex gap-2 ml-4 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <Button
                                            variant="secondary"
                                            onClick={() => viewDetails(record.id)}
                                            className="h-8 w-8 p-0"
                                            title="View Details"
                                        >
                                            <Eye size={16} />
                                        </Button>
                                        <Button
                                            variant="ghost"
                                            onClick={() => deleteRecord(record.id)}
                                            className="h-8 w-8 p-0 hover:text-red-400"
                                            title="Delete"
                                        >
                                            <Trash2 size={16} />
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {/* Details panel */}
                    <div className="lg:col-span-1">
                        {selectedRecord ? (
                            <Card className="sticky top-6">
                                <CardContent className="p-6 space-y-4">
                                    <h3 className="text-xl font-bold text-white mb-4">Details</h3>
                                    {selectedRecord.result && (
                                        <>
                                            <div>
                                                <h4 className="text-xs uppercase tracking-wider font-semibold text-gray-500 mb-1">Title</h4>
                                                <p className="text-white">{selectedRecord.result.title || 'N/A'}</p>
                                            </div>
                                            <div>
                                                <h4 className="text-xs uppercase tracking-wider font-semibold text-gray-500 mb-1">Question</h4>
                                                <p className="text-gray-300 text-sm leading-relaxed">{selectedRecord.result.question || 'N/A'}</p>
                                            </div>
                                            <div>
                                                <h4 className="text-xs uppercase tracking-wider font-semibold text-gray-500 mb-1">Summary</h4>
                                                <p className="text-gray-300 text-sm leading-relaxed">{selectedRecord.result.summary || 'N/A'}</p>
                                            </div>
                                            {selectedRecord.file_generated && (
                                                <div className="pt-4 border-t border-white/10 flex items-center gap-2">
                                                    <FileText size={16} className="text-primary" />
                                                    <span className="text-sm text-gray-400">File Generated</span>
                                                </div>
                                            )}
                                            <Button
                                                onClick={() => setSelectedRecord(null)}
                                                className="w-full mt-4"
                                                variant="secondary"
                                            >
                                                Close
                                            </Button>
                                        </>
                                    )}
                                </CardContent>
                            </Card>
                        ) : (
                            <div className="border border-white/5 rounded-xl p-12 text-center sticky top-6 border-dashed">
                                <Eye size={48} className="mx-auto mb-4 text-gray-700" />
                                <p className="text-gray-500 text-sm">Select a record to view details</p>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}
