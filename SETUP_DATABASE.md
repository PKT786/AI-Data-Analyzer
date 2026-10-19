# Keeping User Accounts Permanently (fixes "asks me to sign up again after restart")

## Why accounts were disappearing

Streamlit Community Cloud erases the app's local files every time the app
restarts, goes to sleep, or is redeployed. Accounts were stored in a local
file (`data/users.db`), so they vanished with it.

The fix is to store accounts in a small online database that lives outside
the app. The code already supports this - you only need to create a free
database and paste its connection URL into your Secrets. It takes about
5 minutes.

> Accounts that were already lost cannot be recovered - those users need to
> sign up one more time. After this setup they will never be lost again.

## Option A - Neon (recommended, free)

1. Go to https://neon.tech and sign up (Google/GitHub login works).
2. Create a new project (any name, e.g. `ai-data-analyzer`).
3. On the project dashboard, find the **Connection string** / **Connect**
   panel and copy the PostgreSQL URL. It looks like:
   `postgresql://myuser:mypassword@ep-something-123.ap-south-1.aws.neon.tech/neondb?sslmode=require`
4. Keep `?sslmode=require` at the end.

## Option B - Supabase (free)

1. Go to https://supabase.com, create a project, and set a database password.
2. Open **Connect** and copy the **Session pooler** connection string
   (not the "Direct connection" one - Streamlit Cloud needs the pooler
   address to connect over IPv4).
3. Replace `[YOUR-PASSWORD]` in it with your real password and add
   `?sslmode=require` at the end if it is not already there.

## Put it in your app

1. Go to https://share.streamlit.io -> your app -> **...** -> **Settings** -> **Secrets**.
2. Add this block (keep any `[google]`, `[facebook]` etc. sections you already have):

   ```toml
   [database]
   url = "postgresql://myuser:mypassword@ep-something-123.ap-south-1.aws.neon.tech/neondb?sslmode=require"
   ```
3. **Save**, then **Reboot app**.
4. Deploy the updated files from this release - `requirements.txt` now
   includes `psycopg2-binary`, which is what talks to the database.

The tables are created automatically on first use. You do not need to run
any SQL.

If your password contains special characters such as `@`, `#`, `/` or `:`,
URL-encode them in the URL (`@` -> `%40`, `#` -> `%23`, `/` -> `%2F`, `:` -> `%3A`).

## How to confirm it worked

1. Open the login page and expand **Login provider setup status (for admin)**.
2. Under **User account storage** you should see:
   *"PostgreSQL database connected - accounts are saved permanently."*
3. Sign up, then use **Reboot app** and log in again - it should simply work.

If you instead see *"Accounts are stored in a temporary local file..."*, the
`[database]` section is missing or misspelled in Secrets.

If you see a connection error, check the URL (password, host, and
`?sslmode=require`). While the URL is configured but unreachable, the app
shows "couldn't reach the account database" rather than silently saving
accounts to the temporary file.
