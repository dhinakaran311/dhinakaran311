import requests
from bs4 import BeautifulSoup
import re

def get_codechef_stats(username):
    url = f"https://www.codechef.com/users/{username}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract stats
        rating_div = soup.find('div', class_='rating-number')
        current_rating = rating_div.text.strip() if rating_div else "N/A"
        
        # Get highest rating
        rating_header = soup.find('div', class_='rating-header')
        highest_rating = "N/A"
        if rating_header:
            highest = rating_header.find('small')
            if highest:
                highest_rating = re.search(r'\d+', highest.text)
                highest_rating = highest_rating.group() if highest_rating else "N/A"
        
        # Get problems solved
        problems_solved = soup.find('h3', string=re.compile('Problems Solved'))
        if problems_solved:
            problems_count = problems_solved.find_next('h5')
            problems_solved = problems_count.text.strip() if problems_count else "N/A"
        else:
            problems_solved = "N/A"
        
        # Contest count (you may need to adjust selector)
        contest_rating = soup.find_all('div', class_='contest-rating')
        contests = len(contest_rating) if contest_rating else "N/A"
        
        return {
            'current_rating': current_rating,
            'highest_rating': highest_rating,
            'problems_solved': problems_solved,
            'contests': contests
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return None

def update_readme(stats):
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update badges using regex
    content = re.sub(
        r'Problems_Solved-\d+',
        f'Problems_Solved-{stats["problems_solved"]}',
        content
    )
    content = re.sub(
        r'Max_Rating-\d+',
        f'Max_Rating-{stats["highest_rating"]}',
        content
    )
    content = re.sub(
        r'Current_Rating-\d+',
        f'Current_Rating-{stats["current_rating"]}',
        content
    )
    content = re.sub(
        r'Contests-\d+',
        f'Contests-{stats["contests"]}',
        content
    )
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    username = "dhinakaran311"
    stats = get_codechef_stats(username)
    
    if stats:
        update_readme(stats)
        print("✅ CodeChef stats updated successfully!")
    else:
        print("❌ Failed to update stats")