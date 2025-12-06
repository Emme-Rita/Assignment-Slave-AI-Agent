import { Bot, CheckCircle, AlertCircle, BookOpen, ShieldCheck, Info } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Alert, AlertTitle, AlertDescription } from '../ui/Alert';
import { clsx } from 'clsx';

interface VerificationResult {
    trust_score: number;
    is_reliable: boolean;
    claims: Array<{
        claim: string;
        status: 'Supported' | 'Contradicted' | 'Unverified';
        reasoning: string;
        source: string;
    }>;
    citations: Array<{
        citation: string;
        status: string;
        note: string;
    }>;
}

interface AnalysisResult {
    title?: string;
    question?: string;
    answer: string;
    summary?: string;
    note?: string;
    more?: string;
    verification?: VerificationResult;
}

interface ResultsDisplayProps {
    result: AnalysisResult | null;
    isLoading: boolean;
}

export function ResultsDisplay({ result, isLoading }: ResultsDisplayProps) {
    if (isLoading) {
        return (
            <div className="space-y-4 animate-pulse">
                <div className="h-64 bg-navy-800 rounded-xl"></div>
                <div className="h-32 bg-navy-800 rounded-xl"></div>
            </div>
        );
    }

    if (!result) return null;

    const getTrustBadgeVariant = (score: number) => {
        if (score >= 0.7) return 'success';
        if (score >= 0.4) return 'warning';
        return 'destructive';
    };

    return (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary/20 text-primary-light rounded-lg">
                        <Bot size={24} />
                    </div>
                    <h2 className="text-xl font-bold text-white">Analysis Results</h2>
                </div>

                {result.verification && (
                    <Badge variant={getTrustBadgeVariant(result.verification.trust_score)} className="gap-2 px-3 py-1.5 text-sm">
                        <ShieldCheck size={16} />
                        Trust Score: {Math.round(result.verification.trust_score * 100)}%
                    </Badge>
                )}
            </div>

            <div className="grid gap-6">
                {result.question && (
                    <Alert>
                        <Info className="h-4 w-4" />
                        <AlertTitle>Identified Question</AlertTitle>
                        <AlertDescription>{result.question}</AlertDescription>
                    </Alert>
                )}

                <Card className="border-primary/30 shadow-primary/10">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-lg">
                            <CheckCircle className="text-green-400" size={20} />
                            Solution
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="prose prose-invert max-w-none text-gray-300">
                            {result.answer}
                        </div>
                    </CardContent>
                </Card>

                {result.verification && result.verification.claims.length > 0 && (
                    <Card className="border-white/10">
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2 text-lg">
                                <BookOpen className="text-blue-400" size={20} />
                                Fact-Check Report
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-3">
                            {result.verification.claims.map((claim, idx) => (
                                <div key={idx} className="p-3 bg-white/5 rounded border border-white/5">
                                    <div className="flex items-start justify-between gap-4">
                                        <p className="text-sm text-gray-200">{claim.claim}</p>
                                        <Badge variant={
                                            claim.status === 'Supported' ? 'success' :
                                                claim.status === 'Contradicted' ? 'destructive' : 'secondary'
                                        }>
                                            {claim.status}
                                        </Badge>
                                    </div>
                                    {claim.reasoning && (
                                        <p className="text-xs text-gray-400 mt-2 pl-2 border-l-2 border-white/10">
                                            {claim.reasoning}
                                        </p>
                                    )}
                                </div>
                            ))}
                        </CardContent>
                    </Card>
                )}

                {result.summary && (
                    <Alert variant="success">
                        <CheckCircle className="h-4 w-4" />
                        <AlertTitle>Summary</AlertTitle>
                        <AlertDescription>{result.summary}</AlertDescription>
                    </Alert>
                )}

                {result.note && (
                    <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Important Note</AlertTitle>
                        <AlertDescription>{result.note}</AlertDescription>
                    </Alert>
                )}
            </div>
        </div>
    );
}

