import { useState, useEffect } from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { AudioPanel } from './components/audio/AudioPanel';
import { ResultsDisplay } from './components/dashboard/ResultsDisplay';
import { Card, CardContent } from './components/ui/Card';
import { Input } from './components/ui/Input';
import { assignmentApi } from './lib/api';
import { GraduationCap, FileText, Feather, Plus, Send, Mic, Loader2 } from 'lucide-react';
import { HistoryView } from './components/history/HistoryView';
import { SettingsView } from './components/settings/SettingsView';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  // Dashboard State
  const [file, setFile] = useState<File | null>(null);
  const [styleSample, setStyleSample] = useState<File | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [instructions, setInstructions] = useState('');
  // Research is now fully automatic and hidden from user control
  const [enableStealth] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [chatHistory, setChatHistory] = useState<any[]>([]);
  const [isDelivering, setIsDelivering] = useState(false);
  const [historyItems, setHistoryItems] = useState<any[]>([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await assignmentApi.getHistory(10);
      setHistoryItems(response.data);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const handleNewChat = () => {
    setResult(null);
    setChatHistory([]);
    setFile(null);
    setAudioBlob(null);
    setInstructions('');
    setActiveTab('dashboard');
  };

  // Execution Fields
  const [studentLevel, setStudentLevel] = useState('Level 100');
  const [department, setDepartment] = useState('Computer Science');
  const [submissionFormat, setSubmissionFormat] = useState('docx');
  const [email, setEmail] = useState('');
  const [whatsapp, setWhatsapp] = useState('');
  const [studentName, setStudentName] = useState('');
  const [matriculeNumber, setMatriculeNumber] = useState('');
  const [schoolName, setSchoolName] = useState('');

  const handleAnalyze = async () => {
    if (!file && !instructions && !audioBlob) return;

    setIsAnalyzing(true);
    setResult(null);

    try {
      const formData = new FormData();
      if (file) formData.append('file', file);
      if (styleSample) formData.append('style_sample', styleSample);
      formData.append('prompt', instructions || '');
      formData.append('use_research', 'true'); // Always enable research
      formData.append('stealth_mode', enableStealth.toString());

      formData.append('student_level', studentLevel);
      formData.append('department', department);
      formData.append('submission_format', submissionFormat);
      if (email) formData.append('email', email);
      if (whatsapp) formData.append('whatsapp', whatsapp);
      if (studentName) formData.append('student_name', studentName);
      if (matriculeNumber) formData.append('matricule_number', matriculeNumber);
      if (schoolName) formData.append('school_name', schoolName);

      if (audioBlob) {
        const audioFile = new File([audioBlob], "voice_note.webm", { type: 'audio/webm' });
        formData.append('voice', audioFile);
      }

      const response = await assignmentApi.refine(formData);
      let parsedResult = response.data;

      if (parsedResult.success) {
        setResult(parsedResult.data);
        setChatHistory([
          { role: 'user', content: instructions || 'Generate assignment solution.' },
          { role: 'assistant', content: parsedResult.data.answer, metadata: parsedResult.data }
        ]);
        // Refresh history to update sidebar
        await fetchHistory();
      } else {
        setResult(parsedResult);
      }

    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Analysis failed. Please try again.';
      alert(`Error: ${errorMsg}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRefine = async (feedback: string) => {
    if (!feedback) return;
    setIsAnalyzing(true);
    try {
      const formData = new FormData();
      if (file) formData.append('file', file);
      if (styleSample) formData.append('style_sample', styleSample);
      formData.append('prompt', feedback);
      formData.append('history', JSON.stringify(chatHistory));
      formData.append('use_research', 'true');
      formData.append('student_level', studentLevel);
      formData.append('department', department);

      const response = await assignmentApi.refine(formData);
      if (response.data.success) {
        const newData = response.data.data;
        setResult(newData);
        setChatHistory([...chatHistory,
        { role: 'user', content: feedback },
        { role: 'assistant', content: newData.answer, metadata: newData }
        ]);
        // Refresh history to update sidebar
        await fetchHistory();
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Refinement failed. Please try again.';
      alert(`Error: ${errorMsg}`);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleDeliver = async () => {
    if (!result) return;
    setIsDelivering(true);
    try {
      const formData = new FormData();
      formData.append('answer', result.answer);
      formData.append('title', result.title || 'Assignment');
      formData.append('question', result.question || '');
      formData.append('summary', result.summary || '');
      // formData.append('research_context', ''); // Optional
      formData.append('student_level', studentLevel);
      formData.append('department', department);
      formData.append('student_name', studentName);
      formData.append('matricule_number', matriculeNumber);
      formData.append('school_name', schoolName);
      formData.append('submission_format', submissionFormat);
      if (email) formData.append('email', email);
      if (whatsapp) formData.append('whatsapp', whatsapp);
      formData.append('stealth_mode', 'true');

      const response = await assignmentApi.deliver(formData);
      if (response.data.success) {
        alert('Assignment successfully finalized and delivered!');
        // Keep the result but mark as delivered
        setResult({ ...result, delivered: true, file_generated: response.data.file_generated });
        // Refresh history to update sidebar
        await fetchHistory();
      }
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || error.message || 'Delivery failed. Please try again.';
      alert(`Error: ${errorMsg}`);
    } finally {
      setIsDelivering(false);
    }
  };

  const renderDashboard = () => (
    <div className={`relative min-h-[calc(100vh-120px)] flex flex-col items-center max-w-4xl mx-auto ${!result && !isAnalyzing ? 'justify-center' : ''}`}>
      {/* Landing View (only shows if no result and not analyzing) */}
      {!result && !isAnalyzing && (
        <div className="w-full space-y-12 animate-in fade-in zoom-in duration-500 pb-32">
          <div className="text-center space-y-4">
            <h1 className="text-5xl font-extrabold text-white tracking-tight">
              What can I help with?
            </h1>
            <p className="text-gray-400 text-lg">Your autonomous agent is ready to handle your assignments.</p>
          </div>

          {/* Profile Info Grid (The "Setup") */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 opacity-80 hover:opacity-100 transition-opacity">
            <Card className="md:col-span-2 border-white/5 bg-navy-800/30 backdrop-blur-sm">
              <CardContent className="p-6 space-y-4">
                <label className="text-sm font-semibold text-primary-light flex items-center gap-2">
                  <GraduationCap className="w-4 h-4" /> Academic Profile
                </label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-1">
                    <label className="text-[10px] uppercase font-bold text-gray-500">Student Name</label>
                    <Input value={studentName} onChange={(e) => setStudentName(e.target.value)} placeholder="John Doe" className="bg-navy-900/50 border-white/5 h-9 text-sm" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] uppercase font-bold text-gray-500">Matricule</label>
                    <Input value={matriculeNumber} onChange={(e) => setMatriculeNumber(e.target.value)} placeholder="FE12A345" className="bg-navy-900/50 border-white/5 h-9 text-sm" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] uppercase font-bold text-gray-500">School</label>
                    <Input value={schoolName} onChange={(e) => setSchoolName(e.target.value)} placeholder="University of Buea" className="bg-navy-900/50 border-white/5 h-9 text-sm" />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="border-white/5 bg-navy-800/30">
              <CardContent className="p-4 space-y-3">
                <label className="text-[10px] uppercase font-bold text-gray-500">Department & Level</label>
                <div className="flex gap-2">
                  <Input value={department} onChange={(e) => setDepartment(e.target.value)} placeholder="Dept" className="bg-navy-900/50 border-white/5 h-9 text-sm flex-1" />
                  <select
                    value={studentLevel}
                    onChange={(e) => setStudentLevel(e.target.value)}
                    className="flex h-9 rounded-md border border-white/5 bg-navy-900/50 px-3 py-1 text-xs text-white focus:outline-none focus:ring-1 focus:ring-primary"
                  >
                    <option value="Level 100">Level 100</option>
                    <option value="Level 200">Level 200</option>
                    <option value="Level 300">Level 300</option>
                    <option value="Level 400">Level 400</option>
                  </select>
                </div>
              </CardContent>
            </Card>

            <Card className="border-white/5 bg-navy-800/30">
              <CardContent className="p-4 space-y-3">
                <label className="text-[10px] uppercase font-bold text-gray-500">Format & Delivery</label>
                <div className="flex gap-2">
                  <select
                    value={submissionFormat}
                    onChange={(e) => setSubmissionFormat(e.target.value)}
                    className="flex h-9 rounded-md border border-white/5 bg-navy-900/50 px-3 py-1 text-xs text-white focus:outline-none focus:ring-1 focus:ring-primary flex-1"
                  >
                    <option value="docx">Word (.docx)</option>
                    <option value="pdf">PDF (.pdf)</option>
                  </select>
                  <div className="flex flex-col gap-2 flex-1">
                    <Input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" className="bg-navy-900/50 border-white/5 h-9 text-sm" />
                    <Input value={whatsapp} onChange={(e) => setWhatsapp(e.target.value)} placeholder="WhatsApp (e.g. +1234567890)" className="bg-navy-900/50 border-white/5 h-9 text-sm" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Results View (Shows the conversation) */}
      {(result || isAnalyzing) && (
        <div className="w-full flex-1 pb-48 pt-4">
          <ResultsDisplay
            history={chatHistory}
            isLoading={isAnalyzing}
          />
        </div>
      )}

      {/* Sleek Bottom Input Bar */}
      <div className="fixed bottom-8 left-0 right-0 md:left-64 flex justify-center px-4 z-50 pointer-events-none">
        <div className="w-full max-w-4xl pointer-events-auto">
          <div className="bg-navy-800/80 backdrop-blur-2xl border border-white/10 rounded-2xl shadow-2xl p-2 flex flex-col gap-2">
            {/* File/Audio Previews can go here */}
            {(file || audioBlob || styleSample) && (
              <div className="flex gap-2 px-2 py-1 border-b border-white/5 mb-1">
                {file && <span className="text-[10px] bg-primary/20 text-primary-light px-2 py-1 rounded-full flex items-center gap-1"><FileText size={10} /> {file.name}</span>}
                {audioBlob && <span className="text-[10px] bg-warning/20 text-warning-light px-2 py-1 rounded-full flex items-center gap-1"><Mic size={10} /> Voice Note Recorded</span>}
                {styleSample && <span className="text-[10px] bg-accent-cyan/20 text-accent-cyan px-2 py-1 rounded-full flex items-center gap-1"><Feather size={10} /> Style: {styleSample.name}</span>}
              </div>
            )}

            <div className="flex items-end gap-2 px-2">
              <div className="flex gap-1 pb-1">
                <label
                  className="p-2 text-gray-400 hover:text-white transition-colors cursor-pointer rounded-lg hover:bg-white/5"
                  title="Attach assignment file (Document/Image)"
                >
                  <Plus size={20} />
                  <input type="file" className="hidden" onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)} />
                </label>
                <label
                  className="p-2 text-gray-400 hover:text-white transition-colors cursor-pointer rounded-lg hover:bg-white/5"
                  title="Upload writing sample for style mirroring (Doppelgänger)"
                >
                  <Feather size={20} />
                  <input type="file" className="hidden" onChange={(e) => setStyleSample(e.target.files ? e.target.files[0] : null)} />
                </label>
              </div>

              <textarea
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                placeholder="Ask anything or paste assignment details..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-white placeholder:text-gray-500 py-3 text-sm resize-none min-h-[44px] max-h-48"
                rows={1}
                onInput={(e) => {
                  const target = e.target as HTMLTextAreaElement;
                  target.style.height = 'auto';
                  target.style.height = target.scrollHeight + 'px';
                }}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    if (result) handleRefine(instructions);
                    else handleAnalyze();
                    setInstructions('');
                  }
                }}
              />

              <div className="flex gap-1 pb-1">
                <AudioPanel
                  onAudioReady={setAudioBlob}
                  compact
                />
                <button
                  onClick={result ? () => handleRefine(instructions) : handleAnalyze}
                  disabled={isAnalyzing || (!file && !instructions && !audioBlob)}
                  className="p-2.5 rounded-xl bg-primary text-white shadow-lg shadow-primary/20 hover:scale-105 active:scale-95 transition-all disabled:opacity-50 disabled:grayscale"
                >
                  {isAnalyzing ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
                </button>
              </div>
            </div>
          </div>
          <p className="text-center text-[10px] text-gray-500 mt-3">
            Free Research Preview. Assignment Agent may provide inaccurate info.
          </p>
        </div>
      </div>
    </div>
  );

  return (
    <MainLayout
      activeTab={activeTab}
      onTabChange={setActiveTab}
      history={historyItems}
      onNewChat={handleNewChat}
      onDeliver={handleDeliver}
      isDelivering={isDelivering}
      canDeliver={!!result && !result.delivered}
    >
      {activeTab === 'dashboard' && renderDashboard()}
      {activeTab === 'history' && <HistoryView />}
      {activeTab === 'settings' && <SettingsView />}
    </MainLayout>
  );
}

export default App;
