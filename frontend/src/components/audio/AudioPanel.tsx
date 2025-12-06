import { useState, useRef } from 'react';
import { Mic, Square, Play, Pause, Trash2 } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card, CardContent } from '../ui/Card';

interface AudioPanelProps {
    onAudioReady: (blob: Blob | null) => void;
}

export function AudioPanel({ onAudioReady }: AudioPanelProps) {
    const [isRecording, setIsRecording] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [duration, setDuration] = useState(0);

    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const audioChunksRef = useRef<Blob[]>([]);
    const audioRef = useRef<HTMLAudioElement | null>(null);
    const timerRef = useRef<any>(null);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                const url = URL.createObjectURL(audioBlob);
                setAudioUrl(url);
                onAudioReady(audioBlob);
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);

            // Start timer
            let seconds = 0;
            timerRef.current = setInterval(() => {
                seconds++;
                setDuration(seconds);
            }, 1000);
        } catch (error) {
            console.error('Error accessing microphone:', error);
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
            if (timerRef.current) {
                clearInterval(timerRef.current);
            }
        }
    };

    const togglePlayback = () => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.pause();
            } else {
                audioRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const deleteAudio = () => {
        setAudioUrl(null);
        onAudioReady(null);
        setDuration(0);
        setIsPlaying(false);
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <Card>
            <CardContent className="p-6 space-y-4">
                <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-white">Voice Instructions</h3>
                    {duration > 0 && <span className="text-sm font-mono text-primary-light">{formatTime(duration)}</span>}
                </div>

                <div className="flex items-center gap-4">
                    {!audioUrl ? (
                        <Button
                            onClick={isRecording ? stopRecording : startRecording}
                            className={`w-12 h-12 rounded-full p-0 flex items-center justify-center ${isRecording ? 'bg-red-500 hover:bg-red-600 animate-pulse' : 'bg-primary hover:bg-primary-dark'
                                }`}
                        >
                            {isRecording ? <Square size={20} /> : <Mic size={20} />}
                        </Button>
                    ) : (
                        <div className="flex items-center gap-3 w-full">
                            <Button onClick={togglePlayback} className="w-10 h-10 rounded-full p-0">
                                {isPlaying ? <Pause size={18} /> : <Play size={18} />}
                            </Button>

                            <div className="flex-1 h-12 bg-white/5 rounded-lg flex items-center justify-center overflow-hidden relative group">
                                {/* Viz Placeholder */}
                                <div className="flex items-center gap-1 h-4">
                                    {[...Array(20)].map((_, i) => (
                                        <div
                                            key={i}
                                            className="w-1 bg-primary-light rounded-full animate-pulse"
                                            style={{
                                                height: `${Math.random() * 100}%`,
                                                animationDelay: `${i * 0.05}s`
                                            }}
                                        />
                                    ))}
                                </div>
                                <audio
                                    ref={audioRef}
                                    src={audioUrl}
                                    onEnded={() => setIsPlaying(false)}
                                    className="hidden"
                                />
                            </div>

                            <Button variant="ghost" onClick={deleteAudio} className="text-red-400 hover:text-red-300">
                                <Trash2 size={20} />
                            </Button>
                        </div>
                    )}

                    {!audioUrl && !isRecording && (
                        <div className="flex-1 text-center text-sm text-gray-400">
                            Tap microphone to record instructions
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}
