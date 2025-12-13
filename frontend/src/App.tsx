import React, { useState } from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { FileUpload } from './components/upload/UploadZone';
import { AudioPanel } from './components/audio/AudioPanel';
import { ResultsDisplay } from './components/dashboard/ResultsDisplay';
import { Button } from './components/ui/Button';
import { Card, CardContent } from './components/ui/Card';
import { Input } from './components/ui/Input';
import { assignmentApi } from './lib/api';
import { Wand2, Loader2, BookOpen, GraduationCap, Mail, FileText, Feather, Settings as SettingsIcon } from 'lucide-react';
import { HistoryView } from './components/history/HistoryView';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  // Dashboard State
  const [file, setFile] = useState<File | null>(null);
  const [styleSample, setStyleSample] = useState<File | null>(null);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [instructions, setInstructions] = useState('');
  // Research is now fully automatic and hidden from user control
  const [enableStealth, setEnableStealth] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Execution Fields
  const [studentLevel, setStudentLevel] = useState('University');
  const [department, setDepartment] = useState('Computer Science');
  const [submissionFormat, setSubmissionFormat] = useState('docx');
  const [email, setEmail] = useState('');
  const [whatsapp, setWhatsapp] = useState('');

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

      if (audioBlob) {
        const audioFile = new File([audioBlob], "voice_note.webm", { type: 'audio/webm' });
        formData.append('voice', audioFile);
      }

      const response = await assignmentApi.execute(formData);
      let parsedResult = response.data; // { success: true, data: {...}, file_generated: "...", ... }

      if (parsedResult.success) {
        // Merge the core data (answer, title) with the metadata (file, verification)
        const mergedResult = {
          ...parsedResult.data,
          file_generated: parsedResult.file_generated,
          verification: parsedResult.verification || parsedResult.data.verification // Handle undefined verification
        };
        setResult(mergedResult);
      } else {
        setResult(parsedResult);
      }

    } catch (error: any) {
      console.error('Execution failed:', error);
      let errorMessage = 'Execution failed. Please try again.';
      if (error.response && error.response.data && error.response.data.detail) {
        const detail = error.response.data.detail;
        if (Array.isArray(detail)) {
          errorMessage = detail.map((e: any) => {
            const field = e.loc ? e.loc[e.loc.length - 1] : 'unknown';
            return `${field}: ${e.msg}`;
          }).join(', ');
        } else if (typeof detail === 'object') {
          errorMessage = `Error: ${JSON.stringify(detail)}`;
        } else {
          errorMessage = `Error: ${detail}`;
        }
      } else if (error.message) {
        errorMessage = `Error: ${error.message}`;
      }
      alert(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderDashboard = () => (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Left Column: Inputs */}
      <div className="lg:col-span-2 space-y-6">
        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-white">New Assignment Task</h1>
          <p className="text-gray-400">Configure your autonomous agent to handle your assignment.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardContent className="p-4 space-y-2">
              <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
                <GraduationCap className="w-4 h-4 text-primary" /> Student Level
              </label>
              <select
                value={studentLevel}
                onChange={(e) => setStudentLevel(e.target.value)}
                className="flex h-10 w-full rounded-md border border-white/10 bg-navy-900 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ring-offset-navy-900"
              >
                <option value="High School">High School</option>
                <option value="University">University (Undergrad)</option>
                <option value="Masters">Master's</option>
                <option value="PhD">PhD</option>
              </select>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 space-y-2">
              <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-primary" /> Department
              </label>
              <Input
                type="text"
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                placeholder="e.g. Computer Science, History"
              />
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 space-y-2">
              <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
                <FileText className="w-4 h-4 text-primary" /> Submission Format
              </label>
              <select
                value={submissionFormat}
                onChange={(e) => setSubmissionFormat(e.target.value)}
                className="flex h-10 w-full rounded-md border border-white/10 bg-navy-900 px-3 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ring-offset-navy-900"
              >
                <option value="docx">Word Document (.docx)</option>
                <option value="pdf">PDF Document (.pdf)</option>
              </select>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4 space-y-2">
              <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
                <Mail className="w-4 h-4 text-primary" /> Delivery (Social)
              </label>
              <div className="space-y-3">
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Email Address"
                />
                <Input
                  type="tel"
                  value={whatsapp}
                  onChange={(e) => setWhatsapp(e.target.value)}
                  placeholder="WhatsApp Number (e.g. +1234567890)"
                />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300">Assignment File</label>
          <FileUpload onFileSelect={setFile} selectedFile={file} />
        </div>

        <Card>
          <CardContent className="p-6 space-y-4">
            <label className="block text-sm font-medium text-gray-300">Assignment Instructions / Prompt</label>
            <textarea
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
              placeholder="Paste the assignment question here..."
              className="flex w-full rounded-md border border-white/10 bg-navy-900 px-3 py-2 text-sm text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 ring-offset-navy-900 min-h-[128px] resize-none"
            />
          </CardContent>
        </Card>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-300 flex items-center gap-2">
            <Feather className="w-4 h-4 text-primary" /> Style Mirroring (Doppelgänger)
          </label>
          <p className="text-xs text-gray-400">Upload a sample of your previous writing (essay, report) to mimic your style.</p>
          <div className="border border-dashed border-gray-600 rounded-lg p-4 bg-navy-900/50 hover:bg-navy-900 transition-colors">
            <input
              type="file"
              onChange={(e) => setStyleSample(e.target.files ? e.target.files[0] : null)}
              className="block w-full text-sm text-gray-400
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-full file:border-0
                      file:text-sm file:font-semibold
                      file:bg-primary/20 file:text-primary
                      hover:file:bg-primary/30
                      cursor-pointer
                    "
            />
            {styleSample && <p className="mt-2 text-sm text-green-400">Selected: {styleSample.name}</p>}
          </div>
        </div>

        <AudioPanel onAudioReady={setAudioBlob} />

        <Card>
          <CardContent className="p-4 flex flex-col gap-3">
            <div className="flex items-center justify-between border-t border-gray-700 pt-3">
              <div className="flex items-center gap-3">
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={enableStealth}
                    onChange={(e) => setEnableStealth(e.target.checked)}
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-700 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-red-500/30 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-red-500"></div>
                  <span className="ml-3 text-sm font-medium text-red-400 flex items-center gap-2">
                    Activate Stealth Mode (Humanizer)
                    <span className="text-xs bg-red-500/20 text-red-300 px-2 py-0.5 rounded-full border border-red-500/30">Bypass Detectors</span>
                  </span>
                </label>
              </div>
            </div>
          </CardContent>
        </Card>

        <Button
          onClick={handleAnalyze}
          disabled={isAnalyzing || (!file && !instructions && !audioBlob)}
          className="w-full h-14 text-lg shadow-xl shadow-primary/20"
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="animate-spin mr-2" /> Executing Assignment Agent...
            </>
          ) : (
            <>
              <Wand2 className="mr-2" /> Start Execution
            </>
          )}
        </Button>
      </div>

      {/* Right Column: Recent or Results */}
      <div className="space-y-6">
        <ResultsDisplay result={result} isLoading={isAnalyzing} />
        {!result && !isAnalyzing && (
          <Card>
            <CardContent className="p-6 text-center">
              <h3 className="font-semibold text-white mb-4">Live Agent Status</h3>
              <p className="text-sm text-gray-400 py-8">Ready to process assignments</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );

  const renderPlaceholder = (title: string, icon: React.ReactNode, message: string) => (
    <Card className="max-w-2xl mx-auto mt-20">
      <CardContent className="p-12 text-center">
        <div className="bg-primary/10 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
          {icon}
        </div>
        <h1 className="text-3xl font-bold text-white mb-4">{title}</h1>
        <p className="text-gray-400 mb-8">{message}</p>
        <Button onClick={() => setActiveTab('dashboard')} className="mx-auto">
          Return to Dashboard
        </Button>
      </CardContent>
    </Card>
  );

  return (
    <MainLayout activeTab={activeTab} onTabChange={setActiveTab}>
      {activeTab === 'dashboard' && renderDashboard()}
      {activeTab === 'upload' && renderDashboard()} {/* Reuse dashboard for upload for now */}
      {activeTab === 'history' && <HistoryView />}
      {activeTab === 'settings' && renderPlaceholder("System Settings", <SettingsIcon size={40} className="text-primary" />, "Configure API keys, default profiles, and system preferences.")}
    </MainLayout>
  );
}

export default App;
