import { LayoutDashboard, Settings, Plus, MessageSquare } from 'lucide-react';
import { clsx } from 'clsx';

interface SidebarProps {
    activeTab: string;
    onTabChange: (tab: string) => void;
    history?: any[];
    onSelectChat?: (id: string) => void;
    onNewChat?: () => void;
}

export function Sidebar({ activeTab, onTabChange, history = [], onNewChat, onSelectChat }: SidebarProps) {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard', color: 'text-primary-light', hoverBg: 'hover:bg-primary/10', activeBg: 'bg-primary/10' },
    ];

    return (
        <aside className="w-64 h-screen border-r border-white/10 bg-navy-900/50 backdrop-blur-xl fixed left-0 top-0 hidden md:flex flex-col">
            <div className="p-4 border-b border-white/10">
                <button
                    onClick={onNewChat}
                    className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 transition-all group mb-2"
                >
                    <Plus size={20} className="text-primary-light" />
                    <span className="font-semibold text-white text-sm">New Chat</span>
                </button>
            </div>

            <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
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
                                "font-medium transition-colors text-sm",
                                isActive ? item.color : "text-gray-400 group-hover:text-white"
                            )}>
                                {item.label}
                            </span>
                        </button>
                    );
                })}

                <div className="pt-4 space-y-2">
                    <p className="px-4 text-[10px] font-bold text-gray-500 uppercase tracking-wider">Your Chats</p>
                    <div className="space-y-1">
                        {history.length > 0 ? (
                            history.map((chat) => (
                                <button
                                    key={chat.id}
                                    className="w-full flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-white/5 transition-all text-left group"
                                    onClick={() => {
                                        if (onSelectChat) onSelectChat(chat.id);
                                    }}
                                >
                                    <MessageSquare size={14} className="text-gray-500 group-hover:text-primary-light" />
                                    <span className="text-xs text-gray-400 group-hover:text-gray-200 truncate pr-2">
                                        {chat.title || chat.prompt || 'Untitled Chat'}
                                    </span>
                                </button>
                            ))
                        ) : (
                            <p className="px-4 py-2 text-[10px] text-gray-600 italic">No recent chats</p>
                        )}
                    </div>
                </div>
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
                        "font-medium transition-colors text-sm",
                        activeTab === 'settings' ? "text-accent-cyan" : "text-gray-400 group-hover:text-white"
                    )}>
                        Settings
                    </span>
                </button>
            </div>
        </aside>
    );
}
