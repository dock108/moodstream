-- MoodStream AI Supabase Schema

-- Profiles table
create table if not exists profiles (
    id uuid primary key references auth.users(id),
    is_premium boolean default false not null,
    preferences jsonb,
    inserted_at timestamptz default now() not null,
    updated_at timestamptz default now() not null
);

-- Content interaction table
create table if not exists user_content (
    id uuid not null references auth.users(id),
    content_id uuid not null,
    content_type text not null,
    status text check (status in ('seen','loved')),
    inserted_at timestamptz default now() not null,
    updated_at timestamptz default now() not null,
    primary key (id, content_id)
);

-- Enable Row Level Security
alter table profiles enable row level security;
alter table user_content enable row level security;

-- RLS policy: allow users to manage their own row
create policy "Profiles are private" on profiles
    for all
    using (auth.uid() = id)
    with check (auth.uid() = id);

create policy "Users manage own content" on user_content
    for all
    using (auth.uid() = id)
    with check (auth.uid() = id);

