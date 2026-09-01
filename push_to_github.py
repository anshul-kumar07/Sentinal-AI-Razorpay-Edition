"""
Sentinel AI 2.0 - GitHub Push Utility
Push your local Git commits directly to GitHub.
"""

import sys
import getpass
import dulwich.porcelain
import dulwich.repo

REPO_PATH = "."

def push_repository():
    print("=" * 60)
    print("  Sentinel AI 2.0 - Push to GitHub")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        remote_url = sys.argv[1]
    else:
        remote_url = input("\nEnter your GitHub repository URL\n(e.g., https://github.com/your-username/sentinel-ai.git): ").strip()
    
    if not remote_url:
        print("Error: Repository URL cannot be empty.")
        return

    repo = dulwich.repo.Repo(REPO_PATH)
    
    # Check / Add remote
    config = repo.get_config()
    section = (b"remote", b"origin")
    config.set(section, b"url", remote_url.encode("utf-8"))
    config.write_to_path()
    print(f"\n[+] Remote 'origin' configured to: {remote_url}")

    # Stage any new changes
    dulwich.porcelain.add(REPO_PATH, paths=["."])
    
    # Try committing if there are unstaged changes
    try:
        dulwich.porcelain.commit(
            REPO_PATH,
            message=b"Update: Sentinel AI 2.0 autonomous multi-agent defense platform",
            author=b"Anshul <anshul@sentinel-ai.local>",
            committer=b"Anshul <anshul@sentinel-ai.local>"
        )
        print("[+] Staged and committed latest changes.")
    except Exception:
        print("[*] Working tree clean. Ready to push.")

    print("\nPushing main branch to GitHub...")
    try:
        dulwich.porcelain.push(repo, remote_url, refspecs=[b"refs/heads/main:refs/heads/main"])
        print("\n[SUCCESS] Successfully pushed Sentinel AI 2.0 to GitHub!")
    except Exception as e:
        print(f"\n[INFO] Direct push returned: {e}")
        print("\nIf GitHub requires authentication, use a Personal Access Token (PAT) format:")
        print(f"  https://<YOUR_GITHUB_TOKEN>@github.com/<USERNAME>/<REPO_NAME>.git")

if __name__ == "__main__":
    push_repository()

