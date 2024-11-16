-- Drop existing table if it exists
DROP TABLE IF EXISTS public.video_summaries;

-- Create video_summaries table
CREATE TABLE public.video_summaries (
    id BIGSERIAL PRIMARY KEY,
    video_id VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    language VARCHAR(2) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_urls TEXT NOT NULL,
    
    -- Add constraints for data validation
    CONSTRAINT valid_language CHECK (language IN ('en', 'ja', 'zh')),
    CONSTRAINT valid_video_id CHECK (length(video_id) > 0)
);

-- Add indexes for common query patterns
CREATE INDEX idx_video_summaries_language ON public.video_summaries(language);
CREATE INDEX idx_video_summaries_timestamp ON public.video_summaries(timestamp DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE public.video_summaries ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Allow public read access"
ON public.video_summaries FOR SELECT
USING (true);

-- Allow authenticated insert
CREATE POLICY "Allow authenticated insert"
ON public.video_summaries FOR INSERT
WITH CHECK (true);
