import os
import requests
from dotenv import load_dotenv
import discord
from linkedin_api import Linkedin

load_dotenv()

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

def search_jobs_linkedin(company_name, num_results=10):
    api = Linkedin(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    jobs = api.search_jobs(company_name=company_name, limit=num_results)
    return jobs

def filter_jobs(job_postings, keywords):
    filtered_jobs = []
    for job in job_postings:
        if any(keyword.lower() in job['title'].lower() or keyword.lower() in job['description'].lower() for keyword in keywords):
            filtered_jobs.append(job)
    return filtered_jobs

def format_job_posting(job):
    return f"**{job['title']}** at {job['company_name']}\nLocation: {job['location']}\nURL: {job['url']}\n\n"

def send_discord_notification(job_postings):
    discord_bot = discord.Client()

    @discord_bot.event
    async def on_ready():
        channel = discord_bot.get_channel(int(DISCORD_CHANNEL_ID))
        if channel:
            message = "**Job Postings Update**\n\n"
            for job in job_postings:
                message += format_job_posting(job)
            await channel.send(message)
        await discord_bot.close()

    discord_bot.run(DISCORD_BOT_TOKEN)

def main():
    company_list = [...]  # Your list of target companies
    keywords = ["Software Engineer", "Data Analyst", "Product Manager"]  # Add your desired keywords

    for company in company_list:
        job_postings = search_jobs_linkedin(company)
        filtered_jobs = filter_jobs(job_postings, keywords)
        if filtered_jobs:
            send_discord_notification(filtered_jobs)

if __name__ == "__main__":
    main()