# ezDecline

Hi :D

**Tired of rejecting invitations with low **Response Efficiency Rate** in Hackerone one by one?**

### Well...same here!!!

When I checked my **Pending Invitations** a few days ago, coming back from a long break from bug bounty. I saw a bunched of invitations I don't even want to check because their **Response Efficiency Rate(RER)** was so bad, so I started rejecting them one by one...it was not a great experience, so I decided to make this ezDecline to automatically reject invites you don't want based on the Program **Response Efficiency Rate(RER)**

I hope you guys will find this helpful :D

### Usage
1. Git clone the repository - `git clone https://github.com/SoloType14/ezDecline.git`
2. Get your session(__Host-session) from Hackerone
   * `Chrome Dev Tools` ---> `Application` ---> `Cookies` ---> `https://hackerone.com` ---> ` __Host-session` or anything that will let you get the value of __Host-session  
3. Run the python file - example: `python3 ezDecline.py` (Make sure you have the **requests** module installed in python - `pip3 install requests`)
     * Paste your `__Host-session`
     * Type the value of the Response Efficiency Rate you want to decline(downwards)
     * Done!!! (Make sure to double check in the website if it was indeed successful)

## Disclaimer - I'm not an expert in coding so the code can be ugly...but it works so...it's good to me :P




https://github.com/user-attachments/assets/34e25d7b-0044-4708-bff8-18d7ff95695e



