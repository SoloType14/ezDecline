import requests
from requests.structures import CaseInsensitiveDict
import re

#For debugging purposes
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def getCookies():
    getCookies.host_session = input("Please paste the value of your __Host-session here: ")
    getX_CSRF_TOKEN()

def getX_CSRF_TOKEN():

    url = "https://hackerone.com//opportunities/all"
    headers = CaseInsensitiveDict()
    headers = {"Cookie": "__Host-session="+ getCookies.host_session}

    response = requests.get(url=url,headers=headers,allow_redirects=False,proxies=proxies, verify=False) 

    response_content = response.text

    match = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']\s*/?>', response_content)

    # Check if a match was found
    if match:
        getX_CSRF_TOKEN.x_csrf_token = match.group(1)  # Extract the content attribute value
        print(f"X-CSRF-Token: {getX_CSRF_TOKEN.x_csrf_token}")
    else:
        print("CSRF token not found.")


    getPendingInvites()


def getPendingInvites():

    url = "https://hackerone.com/graphql"
    body = {"operationName":"PrivateProgramInvitationsQuery","variables":{"count":1000,"orderBy":{"field":"invitation_expires_at","direction":"ASC"},"product_area":"opportunity_discovery","product_feature":"pending_invitations"},"query":"query PrivateProgramInvitationsQuery($count: Int, $orderBy: InvitationOrderInput, $cursor: String) {\n  me {\n    id\n    hacker_invitations_profile {\n      id\n      receive_invites\n      __typename\n    }\n    soft_launch_invitations(\n      first: $count\n      after: $cursor\n      state: open\n      order_by: $orderBy\n    ) {\n      pageInfo {\n        endCursor\n        hasNextPage\n        __typename\n      }\n      edges {\n        node {\n          id\n          expires_at\n          token\n          team {\n            id\n            handle\n            submission_requirements {\n              id\n              terms_required_at\n              mfa_required_at\n              __typename\n            }\n            ...TeamTableResponseEfficiency\n            ...TeamTableLaunchDate\n            ...TeamTableResolvedReports\n            ...TeamTableMinimumBounty\n            ...TeamTableAverageBounty\n            ...TeamTableAvatarAndTitle\n            __typename\n          }\n          ...InvitationLink\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TeamTableResponseEfficiency on Team {\n  id\n  response_efficiency_percentage\n  ...ResponseEfficiencyIndicator\n  __typename\n}\n\nfragment ResponseEfficiencyIndicator on Team {\n  id\n  response_efficiency_percentage\n  __typename\n}\n\nfragment TeamTableLaunchDate on Team {\n  id\n  launched_at\n  __typename\n}\n\nfragment TeamTableResolvedReports on Team {\n  id\n  resolved_report_count\n  __typename\n}\n\nfragment TeamTableMinimumBounty on Team {\n  id\n  currency\n  base_bounty\n  __typename\n}\n\nfragment TeamTableAverageBounty on Team {\n  id\n  currency\n  average_bounty_lower_amount\n  average_bounty_upper_amount\n  __typename\n}\n\nfragment TeamTableAvatarAndTitle on Team {\n  id\n  profile_picture(size: medium)\n  name\n  handle\n  submission_state\n  triage_active\n  publicly_visible_retesting\n  state\n  allows_bounty_splitting\n  external_program {\n    id\n    __typename\n  }\n  ...TeamLinkWithMiniProfile\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n\nfragment InvitationLink on InvitationInterface {\n  ... on InvitationsSoftLaunch {\n    id\n    token\n    team {\n      id\n      handle\n      submission_requirements {\n        id\n        terms_required_at\n        mfa_required_at\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on InvitationsRetest {\n    id\n    token\n    accepted_at\n    team {\n      id\n      handle\n      submission_requirements {\n        id\n        terms_required_at\n        mfa_required_at\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
 
    headers = CaseInsensitiveDict()
    headers = {"x-csrf-token": getX_CSRF_TOKEN.x_csrf_token, "Cookie": "__Host-session="+ getCookies.host_session}


    response = requests.post(url=url, json=body,headers=headers,allow_redirects=False,proxies=proxies, verify=False) 

    if response.status_code == 200: 
        data = response.json()

        #Filter the json response

        # Get the list of invitations from 'edges' inside 'soft_launch_invitations'
        invitations = data['data']['me']['soft_launch_invitations']['edges']

        #Ask for the REP value you want to decline
        badREF = int(input("Enter the Response Efficiency Percentage you want to decline (downwards): "))

        
        # Filter the invitations where response_efficiency_percentage > 80
        filtered_companies = [
            invitation['node'] for invitation in invitations
            if invitation['node']['team']['response_efficiency_percentage'] <= badREF
        ]

        # Extract and print the 'name', 'response_efficiency_percentage', and 'token' for each company
        for company in filtered_companies:
            name = company['team']['name']  # Company's name
            response_rate = company['team']['response_efficiency_percentage']  # Response rate
            token = company['token']  # Token will be used to decline the invitation later
            
            # Print the extracted values
            print("All of the invitation from listed companies will be declined")

            print(f"Company Name: {name}")
            print(f"Response Rate: {response_rate}")
            print('---')
                

    else:
        print(f"Failed to retrieve list of invitation - Status code: {response.status_code}")



        
def main():
    getCookies()


if __name__ == "__main__":
    main()