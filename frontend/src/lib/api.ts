import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const assignmentApi = {
    analyze: (formData: FormData) =>
        api.post('/analyze', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }),

    analyzeWithVoice: (formData: FormData) =>
        api.post('/analyze-with-voice', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }),

    execute: (formData: FormData) =>
        api.post('/execute', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }),

    refine: (formData: FormData) =>
        api.post('/refine', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }),

    deliver: (formData: FormData) =>
        api.post('/deliver', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }),

    research: (query: string) =>
        api.post('/research/research', { query }),

    getDownloadUrl: (filename: string) =>
        `http://localhost:8000/api/v1/download/${filename}`,

    getHistory: (limit: number = 50) =>
        api.get(`/history?limit=${limit}`),

    getHistoryDetails: (recordId: string) =>
        api.get(`/history/${recordId}`),

    deleteHistory: (recordId: string) =>
        api.delete(`/history/${recordId}`)
};

export default api;
