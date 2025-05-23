# Supabase Setup

This guide describes how to configure Supabase for MoodStream AI.

## 1. Create a Supabase project
1. Sign in to the [Supabase dashboard](https://app.supabase.com/).
2. Create a new project and note the **Project URL** and **Anon Key**.

## 2. Enable Authentication
1. In the **Authentication** settings enable **Email/Password** with **Magic Link**.
2. (Optional) Enable the Google OAuth provider and supply your Google credentials.

## 3. Profiles Table
1. Create a table named `profiles`.
2. Add a `uuid` primary key column that references `auth.users.id`.
3. Add any extra fields you need such as `username` and `is_premium` (boolean).
4. Enable **Row Level Security** on the table and add a policy allowing users to
   read and update only their own row.

```sql
-- Example policy
create policy "Users can manage their profile" on profiles
  for all using ( auth.uid() = id )
  with check ( auth.uid() = id );
```
## 4. User Content Table
1. Create a table named `user_content` to track interactions with recommended content.
2. Use `docs/db/schema.sql` as a reference or run it directly in the SQL editor.
3. Columns include `id` referencing `auth.users.id`, `content_id`, `content_type`, and a `status` field (`seen` or `loved`).
4. Enable **Row Level Security** with a policy restricting access to rows where `id = auth.uid()`.

## 5. Apply Schema
Run the SQL file located at `docs/db/schema.sql` in the Supabase SQL editor to create the tables and policies described above.


## 6. Service Role Key
1. From **Project Settings → API**, create a **Service Role** key.
2. Store the project URL, anon key, and service role key in a `.env` file as
   shown below.

```env
SUPABASE_URL=<project-url>
SUPABASE_ANON_KEY=<public-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
```

Copy `backend/.env.example` to `.env` and fill in these values.

## 7. Test Users
Create a few test users through the dashboard or the authentication API. A row
in `profiles` will be created automatically for each user.

## 8. Frontend Integration
The frontend should use the anon key to sign up, sign in, and sign out users.
The backend can use the service role key for administrative tasks.
