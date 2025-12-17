import React from 'react';
import { Sidebar } from './Sidebar';
import { Search, User, Bell } from 'lucide-react';
import { Input } from '../ui/Input';

interface MainLayoutProps {
    children: React.ReactNode;
    activeTab: string;
    onTabChange: (tab: string) => void;
}

export function MainLayout({ children, activeTab, onTabChange }: MainLayoutProps) {
    return (
        <div className="min-h-screen bg-background text-foreground flex">
            <Sidebar activeTab={activeTab} onTabChange={onTabChange} />

            <main className="flex-1 md:ml-64 relative">
                {/* Solid Background */}
                <div className="fixed top-0 left-0 w-full h-full bg-background -z-10 pointer-events-none" />

                {/* Top Header */}
                <header className="sticky top-0 z-50 px-8 py-4 flex items-center justify-between backdrop-blur-sm bg-background/50 border-b border-border">
                    <div className="flex-1 max-w-xl">
                        <Input
                            leftIcon={<Search size={18} />}
                            placeholder="Search assignments..."
                            className="bg-secondary/50 border-border focus:border-primary/50"
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    alert("Global search is coming soon! Please use the Dashboard for now.");
                                }
                            }}
                        />
                    </div>

                    <div className="flex items-center gap-4 ml-4">
                        <button className="p-2 text-muted-foreground hover:text-foreground transition-colors relative">
                            <Bell size={20} />
                            <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full" />
                        </button>
                        <div className="w-8 h-8 rounded-full bg-primary/20 border border-primary/50 flex items-center justify-center">
                            <User size={16} className="text-primary-light" />
                        </div>
                    </div>
                </header>

                <div className="p-8 max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
}
