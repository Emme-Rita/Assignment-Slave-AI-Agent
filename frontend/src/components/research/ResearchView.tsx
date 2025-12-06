import { useState } from 'react';
import { Search, Loader2, ExternalLink } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { Input } from '../ui/Input';
import { Badge } from '../ui/Badge';
import { assignmentApi } from '../../lib/api';

export function ResearchView() {
    const [query, setQuery] = useState('');
    const [isSearching, setIsSearching] = useState(false);
    const [results, setResults] = useState<any>(null);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setIsSearching(true);
        setResults(null);

        try {
            const response = await assignmentApi.research(query);
            if (response.data.success) {
                setResults(response.data.data);
            }
        } catch (error) {
            console.error(error);
            alert("Research failed. Please try again.");
        } finally {
            setIsSearching(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-white">Research Center</h1>
                <p className="text-gray-400">Autonomous web research agent.</p>
            </div>

            <Card>
                <CardContent className="p-6 flex gap-4">
                    <Input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                        placeholder="Enter a topic to research (e.g., 'Quantum Computing advancements 2024')..."
                        leftIcon={<Search size={18} />}
                        className="flex-1 border-primary/20 focus:border-primary/50"
                    />
                    <Button
                        onClick={handleSearch}
                        disabled={isSearching}
                        className="w-32 bg-accent-purple hover:bg-accent-purple/90 shadow-accent-purple/20"
                    >
                        {isSearching ? <Loader2 className="animate-spin" /> : <Search />}
                        Search
                    </Button>
                </CardContent>
            </Card>

            {results && (
                <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
                    <Card className="bg-primary/5 border-primary/20">
                        <CardHeader>
                            <CardTitle className="text-primary-light">AI Summary</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="prose prose-invert max-w-none">
                                <p className="whitespace-pre-line text-gray-200">{results.summary}</p>
                            </div>
                        </CardContent>
                    </Card>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {results.sources.map((source: any, i: number) => (
                            <a
                                key={i}
                                href={source.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="group block"
                            >
                                <Card className="h-full hover:bg-white/5 transition-colors border-white/5">
                                    <CardContent className="p-4">
                                        <div className="flex items-start justify-between mb-2">
                                            <h4 className="font-semibold text-white group-hover:text-primary-light truncate pr-4">{source.title}</h4>
                                            <ExternalLink size={16} className="text-gray-500 group-hover:text-white" />
                                        </div>
                                        <p className="text-sm text-gray-400 mt-2 line-clamp-3 mb-3">{source.content}</p>
                                        <div className="flex items-center gap-2">
                                            <Badge variant="secondary">Source {i + 1}</Badge>
                                            {source.score > 0.5 && (
                                                <Badge variant="success">High Relevance</Badge>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            </a>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
