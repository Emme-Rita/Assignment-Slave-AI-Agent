import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8001/api/v1',
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

    research: (query: string) =>
        api.post('/research/research', { query }),
};

export default api;
