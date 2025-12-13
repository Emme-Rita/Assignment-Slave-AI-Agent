import { LayoutDashboard, FileText, History, Settings } from 'lucide-react';
import { clsx } from 'clsx';

interface SidebarProps {
    activeTab: string;
    onTabChange: (tab: string) => void;
}

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard', color: 'text-primary-light', hoverBg: 'hover:bg-primary/10', activeBg: 'bg-primary/10' },
        { icon: FileText, label: 'Upload Assignment', id: 'upload', color: 'text-success-light', hoverBg: 'hover:bg-success/10', activeBg: 'bg-success/10' },
        { icon: History, label: 'History', id: 'history', color: 'text-warning-light', hoverBg: 'hover:bg-warning/10', activeBg: 'bg-warning/10' },
    ];

    return (
        <aside className="w-64 h-screen border-r border-white/10 bg-navy-900/50 backdrop-blur-xl fixed left-0 top-0 hidden md:flex flex-col">
            <div className="p-6 border-b border-white/10">
                <h1 className="text-xl font-bold text-white tracking-tight">
                    Assignment Helper
                </h1>
            </div>

            <nav className="flex-1 p-4 space-y-2">
                {navItems.map((item) => {
                    const isActive = activeTab === item.id;
                    return (
                        <button
                            key={item.id}
                            onClick={() => onTabChange(item.id)}
                            className={clsx(
                                "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all group",
                                isActive ? item.activeBg : "hover:bg-white/5"
                            )}
                        >
                            <item.icon
                                size={20}
                                className={clsx(
                                    "transition-colors",
                                    isActive ? item.color : "text-gray-400 group-hover:text-white"
                                )}
                            />
                            <span className={clsx(
                                "font-medium transition-colors",
                                isActive ? item.color : "text-gray-400 group-hover:text-white"
                            )}>
                                {item.label}
                            </span>
                        </button>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-white/10">
                <button
                    onClick={() => onTabChange('settings')}
                    className={clsx(
                        "w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all group",
                        activeTab === 'settings' ? "bg-accent-cyan/10" : "hover:bg-white/5"
                    )}
                >
                    <Settings
                        size={20}
                        className={clsx(
                            "transition-colors",
                            activeTab === 'settings' ? "text-accent-cyan" : "text-gray-400 group-hover:text-white"
                        )}
                    />
                    <span className={clsx(
                        "font-medium transition-colors",
                        activeTab === 'settings' ? "text-accent-cyan" : "text-gray-400 group-hover:text-white"
                    )}>
                        Settings
                    </span>
                </button>
            </div>
        </aside>
    );
}
