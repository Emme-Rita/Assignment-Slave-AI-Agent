# API Troubleshooting Guide

## Common Issues and Solutions

### 1. Invalid API Key Error ✅ FIXED

**Problem**: Getting "Invalid API Key" error when testing endpoints

**Root Cause**: The `.env` file had quotes around the API key values. When `python-dotenv` loads environment variables, it includes the quotes as part of the value, causing authentication to fail.

**Solution**: Remove quotes from all values in the `.env` file

**Before** (❌ Incorrect):
```bash
GEMINI_API_KEY="AIzaSyD1bjH0gljF19uV9gUtSU-d2u-IXCWuDWY"
TAVILY_API_KEY="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"
```

**After** (✅ Correct):
```bash
GEMINI_API_KEY=AIzaSyD1bjH0gljF19uV9gUtSU-d2u-IXCWuDWY
TAVILY_API_KEY=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
```

**Important**: After changing the `.env` file, you MUST restart the server for changes to take effect.

---

### 2. Server Not Picking Up Changes

**Problem**: Changes to `.env` file not reflected in the API

**Solution**: 
1. Stop the server (Ctrl+C)
2. Restart with: `python -m uvicorn app.main:app --reload`

---

### 3. File Upload Issues

**Problem**: File upload fails or returns errors

**Common Causes**:
- File size exceeds 10MB limit
- File type not supported (only PDF, Word, Images allowed)
- Incorrect form field names

**Solution**:
- Check file size: `ls -lh yourfile.pdf`
- Verify file type is supported
- Use correct form field names: `file` and `prompt`

**Example with curl**:
```bash
curl -X POST "http://localhost:8000/api/v1/assignment/analyze" \
  -F "file=@assignment.pdf" \
  -F "prompt=Solve this problem" \
  -F "use_research=false"
```

---

### 4. PDF/Word Text Extraction Fails

**Problem**: Cannot extract text from uploaded files

**Possible Causes**:
- Corrupted file
- Password-protected PDF
- Scanned PDF (image-based, not text)

**Solution**:
- Ensure PDF contains actual text (not just images)
- Remove password protection
- For scanned PDFs, consider using OCR preprocessing

---

### 5. Gemini API Errors

**Common Error Messages**:
- `Invalid API key`: Check `.env` file (no quotes!)
- `Quota exceeded`: Check your Google Cloud quota
- `Model not found`: Verify model name is `gemini-1.5-pro`

**Debugging Steps**:
1. Verify API key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check `.env` file has no quotes
3. Restart server after any `.env` changes

---

### 6. Tavily Search Errors

**Common Issues**:
- Invalid API key
- Rate limit exceeded
- Network connectivity issues

**Solution**:
1. Verify Tavily API key at [Tavily Dashboard](https://tavily.com)
2. Check rate limits on your plan
3. Test with smaller `max_results` value

---

## Testing Checklist

Use this checklist to verify your setup:

- [ ] `.env` file exists in `backend/` directory
- [ ] API keys in `.env` have NO quotes
- [ ] Server is running on http://localhost:8000
- [ ] Health endpoint returns 200: `curl http://localhost:8000/health`
- [ ] Swagger UI accessible at http://localhost:8000/docs
- [ ] Research endpoint works (test with simple query)
- [ ] File upload accepts PDF/Word/Image files

---

## Quick Test Commands

### Test Health
```bash
curl http://localhost:8000/health
```

### Test Research
```bash
curl -X POST "http://localhost:8000/api/v1/research/research" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "max_results": 3}'
```

### Test File Upload (with text file)
```bash
echo "What is 2+2?" > test.txt
curl -X POST "http://localhost:8000/api/v1/assignment/analyze" \
  -F "file=@test.txt" \
  -F "prompt=Solve this" \
  -F "use_research=false"
```

---

## Verified Working ✅

The following has been tested and confirmed working:
- ✅ Health endpoint
- ✅ Research endpoint with Tavily integration
- ✅ Environment variable loading (after fix)
- ✅ Server startup and reload

---

## Need More Help?

1. Check server logs in the terminal where uvicorn is running
2. Visit Swagger UI at http://localhost:8000/docs for interactive testing
3. Review the error response JSON for specific error messages
4. Ensure all dependencies are installed: `pip install -r requirements.txt`
