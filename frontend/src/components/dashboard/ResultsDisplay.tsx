import { Bot, CheckCircle, ShieldCheck, Download, Info } from 'lucide-react';
import { Card, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { Alert, AlertTitle, AlertDescription } from '../ui/Alert';
import { assignmentApi } from '../../lib/api';

interface ResultsDisplayProps {
    history: any[];
    isLoading: boolean;
}

export function ResultsDisplay({ history, isLoading }: ResultsDisplayProps) {

    if (isLoading && history.length === 0) {
        return (
            <div className="space-y-4 animate-pulse">
                <div className="h-64 bg-navy-800 rounded-xl px-6 py-8">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="w-10 h-10 bg-white/5 rounded-lg animate-pulse" />
                        <div className="h-6 w-32 bg-white/5 rounded animate-pulse" />
                    </div>
                    <div className="space-y-3">
                        <div className="h-4 w-full bg-white/5 rounded animate-pulse" />
                        <div className="h-4 w-5/6 bg-white/5 rounded animate-pulse" />
                        <div className="h-4 w-4/6 bg-white/5 rounded animate-pulse" />
                    </div>
                </div>
            </div>
        );
    }

    const getTrustBadgeVariant = (score: number) => {
        if (score >= 0.7) return 'success';
        if (score >= 0.4) return 'warning';
        return 'destructive';
    };

    const handleDownload = (file_generated?: string) => {
        if (file_generated) {
            const filename = file_generated.split(/[\\/]/).pop();
            if (filename) {
                window.open(assignmentApi.getDownloadUrl(filename), '_blank');
            }
        }
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto">
            {history.map((msg, idx) => (
                <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                    {msg.role === 'user' ? (
                        <div className="bg-navy-800/80 backdrop-blur-sm border border-white/5 rounded-2xl px-5 py-3 max-w-[80%] text-gray-200 text-sm shadow-xl">
                            {msg.content}
                        </div>
                    ) : (
                        <div className="w-full space-y-6">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-primary/20 text-primary-light rounded-lg">
                                        <Bot size={20} />
                                    </div>
                                    <h2 className="text-sm font-bold text-gray-400">Response</h2>
                                </div>

                                <div className="flex items-center gap-2">
                                    {msg.metadata?.file_generated && (
                                        <Button
                                            variant="secondary"
                                            onClick={() => handleDownload(msg.metadata.file_generated)}
                                            className="h-8 gap-2 bg-navy-800 border border-white/10 hover:bg-navy-700 text-xs px-3"
                                        >
                                            <Download size={14} />
                                            Download
                                        </Button>
                                    )}

                                    {msg.metadata?.verification && (
                                        <Badge variant={getTrustBadgeVariant(msg.metadata.verification.trust_score)} className="gap-2 px-2 py-1 text-[10px]">
                                            <ShieldCheck size={12} />
                                            Trust: {Math.round(msg.metadata.verification.trust_score * 100)}%
                                        </Badge>
                                    )}
                                </div>
                            </div>

                            <div className="grid gap-6">
                                {msg.metadata?.question && (
                                    <Alert className="bg-navy-800/50 border-white/5 py-3">
                                        <Info className="h-4 w-4 text-blue-400" />
                                        <AlertTitle className="text-blue-400 text-[10px] font-bold uppercase tracking-wider">Identified Question</AlertTitle>
                                        <AlertDescription className="text-gray-300 text-xs mt-1 leading-relaxed">
                                            {msg.metadata.question}
                                        </AlertDescription>
                                    </Alert>
                                )}

                                <Card className="border-primary/20 shadow-primary/5 overflow-hidden bg-navy-800/20">
                                    <CardContent className="p-0">
                                        <div className="p-6 prose prose-invert max-w-none text-gray-300 bg-navy-950/20 whitespace-pre-wrap font-sans text-sm leading-relaxed">
                                            {msg.content}
                                        </div>
                                    </CardContent>
                                </Card>

                                {msg.metadata?.summary && (
                                    <Alert variant="success" className="bg-green-500/5 border-green-500/10 py-3">
                                        <CheckCircle className="h-3 w-3 text-green-400" />
                                        <AlertTitle className="text-green-400 text-[10px] font-bold uppercase tracking-wider">Summary</AlertTitle>
                                        <AlertDescription className="text-gray-400 text-[11px] mt-1">{msg.metadata.summary}</AlertDescription>
                                    </Alert>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            ))}

            {isLoading && (
                <div className="flex items-center gap-3 animate-pulse pt-4">
                    <div className="p-2 bg-primary/10 text-primary/50 rounded-lg">
                        <Bot size={20} />
                    </div>
                    <div className="space-y-2">
                        <div className="h-2 w-24 bg-white/5 rounded" />
                        <div className="h-2 w-32 bg-white/5 rounded" />
                    </div>
                </div>
            )}
        </div>
    );
}
