import React, { useEffect, useState } from 'react';
import { Moon, Sun, Monitor, Save, RotateCcw } from 'lucide-react';
import { Button } from '../ui/Button';
import { Card, CardContent } from '../ui/Card';
import { useTheme } from '../ui/theme-provider';

export function SettingsView() {
    const { setTheme, theme } = useTheme();
    const [defaultLevel, setDefaultLevel] = useState('University');
    const [defaultDepartment, setDefaultDepartment] = useState('Computer Science');
    const [defaultFormat, setDefaultFormat] = useState('docx');
    const [showSuccess, setShowSuccess] = useState(false);

    useEffect(() => {
        // Load settings
        const loadedLevel = localStorage.getItem('default_student_level');
        const loadedDept = localStorage.getItem('default_department');
        const loadedFormat = localStorage.getItem('default_submission_format');

        if (loadedLevel) setDefaultLevel(loadedLevel);
        if (loadedDept) setDefaultDepartment(loadedDept);
        if (loadedFormat) setDefaultFormat(loadedFormat);
    }, []);

    const handleSave = () => {
        localStorage.setItem('default_student_level', defaultLevel);
        localStorage.setItem('default_department', defaultDepartment);
        localStorage.setItem('default_submission_format', defaultFormat);

        setShowSuccess(true);
        setTimeout(() => setShowSuccess(false), 2000);
    };

    const handleReset = () => {
        if (confirm("Reset all settings to default?")) {
            localStorage.removeItem('default_student_level');
            localStorage.removeItem('default_department');
            localStorage.removeItem('default_submission_format');
            setDefaultLevel('University');
            setDefaultDepartment('Computer Science');
            setDefaultFormat('docx');
            setTheme("system");
        }
    }

    return (
        <div className="space-y-6 max-w-4xl mx-auto">
            <div className="space-y-2">
                <h1 className="text-3xl font-bold text-white dark:text-white text-navy-900">System Settings</h1>
                <p className="text-gray-400">Configure appearance and default behaviors</p>
            </div>

            <div className="grid grid-cols-1 gap-6">
                {/* Appearance Section */}
                <Card>
                    <CardContent className="p-6 space-y-4">
                        <h2 className="text-xl font-semibold text-white mb-4">Appearance</h2>
                        <div className="grid grid-cols-3 gap-4">
                            <button
                                onClick={() => setTheme("light")}
                                className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all ${theme === "light"
                                        ? "border-primary bg-primary/10"
                                        : "border-gray-700 bg-navy-900/50 hover:bg-navy-800"
                                    }`}
                            >
                                <Sun className="w-8 h-8 mb-2 text-yellow-500" />
                                <span className="text-sm font-medium text-white">Light</span>
                            </button>
                            <button
                                onClick={() => setTheme("dark")}
                                className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all ${theme === "dark"
                                        ? "border-primary bg-primary/10"
                                        : "border-gray-700 bg-navy-900/50 hover:bg-navy-800"
                                    }`}
                            >
                                <Moon className="w-8 h-8 mb-2 text-purple-400" />
                                <span className="text-sm font-medium text-white">Dark</span>
                            </button>
                            <button
                                onClick={() => setTheme("system")}
                                className={`flex flex-col items-center justify-center p-4 rounded-lg border-2 transition-all ${theme === "system"
                                        ? "border-primary bg-primary/10"
                                        : "border-gray-700 bg-navy-900/50 hover:bg-navy-800"
                                    }`}
                            >
                                <Monitor className="w-8 h-8 mb-2 text-blue-400" />
                                <span className="text-sm font-medium text-white">System</span>
                            </button>
                        </div>
                    </CardContent>
                </Card>

                {/* Default Profiles Section */}
                <Card>
                    <CardContent className="p-6 space-y-4">
                        <h2 className="text-xl font-semibold text-white mb-4">Default Profile</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-gray-300">Default Student Level</label>
                                <select
                                    value={defaultLevel}
                                    onChange={(e) => setDefaultLevel(e.target.value)}
                                    className="flex h-10 w-full rounded-md border border-white/10 bg-navy-900 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary"
                                >
                                    <option value="High School">High School</option>
                                    <option value="University">University</option>
                                    <option value="Masters">Master's</option>
                                    <option value="PhD">PhD</option>
                                </select>
                            </div>

                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-gray-300">Default Department</label>
                                <input
                                    type="text"
                                    value={defaultDepartment}
                                    onChange={(e) => setDefaultDepartment(e.target.value)}
                                    className="flex h-10 w-full rounded-md border border-white/10 bg-navy-900 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary"
                                />
                            </div>

                            <div className="space-y-2">
                                <label className="block text-sm font-medium text-gray-300">Default Output Format</label>
                                <select
                                    value={defaultFormat}
                                    onChange={(e) => setDefaultFormat(e.target.value)}
                                    className="flex h-10 w-full rounded-md border border-white/10 bg-navy-900 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary"
                                >
                                    <option value="docx">Word (.docx)</option>
                                    <option value="pdf">PDF (.pdf)</option>
                                </select>
                            </div>
                        </div>

                        <div className="pt-6 flex gap-4">
                            <Button onClick={handleSave} className="flex-1 gap-2">
                                <Save size={16} /> Save Settings
                            </Button>
                            <Button onClick={handleReset} variant="secondary" className="gap-2">
                                <RotateCcw size={16} /> Reset
                            </Button>
                        </div>
                        {showSuccess && (
                            <div className="p-3 bg-green-500/20 text-green-300 text-sm rounded-md text-center animate-in fade-in">
                                Settings saved successfully!
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
