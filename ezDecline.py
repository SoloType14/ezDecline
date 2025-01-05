import requests
from requests.structures import CaseInsensitiveDict
import re


def getX_CSRF_TOKEN():

    host_session = input("Please paste the value of your __Host-session here: ")

    url = "https://hackerone.com//opportunities/all"
    headers = CaseInsensitiveDict()
    headers = {"Cookie": "__Host-session="+ host_session}

    response = requests.get(url=url,headers=headers,allow_redirects=False) 

    response_content = response.text

    match = re.search(r'<meta\s+name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']\s*/?>', response_content)

    # Check if a match was found
    if match:
        x_csrf_token = match.group(1)  # Extract the content attribute value
        #print(f"X-CSRF-Token: {x_csrf_token}")
    else:
        print("CSRF token not found.")

    final_header = { "Cookie": "__Host-session="+ host_session, "x-csrf-token": x_csrf_token}

    getPendingInvites(final_header)


def getPendingInvites(final_header):

    url = "https://hackerone.com/graphql"
    body = {"operationName":"PrivateProgramInvitationsQuery","variables":{"count":1000,"orderBy":{"field":"invitation_expires_at","direction":"ASC"},"product_area":"opportunity_discovery","product_feature":"pending_invitations"},"query":"query PrivateProgramInvitationsQuery($count: Int, $orderBy: InvitationOrderInput, $cursor: String) {\n  me {\n    id\n    hacker_invitations_profile {\n      id\n      receive_invites\n      __typename\n    }\n    soft_launch_invitations(\n      first: $count\n      after: $cursor\n      state: open\n      order_by: $orderBy\n    ) {\n      pageInfo {\n        endCursor\n        hasNextPage\n        __typename\n      }\n      edges {\n        node {\n          id\n          expires_at\n          token\n          team {\n            id\n            handle\n            submission_requirements {\n              id\n              terms_required_at\n              mfa_required_at\n              __typename\n            }\n            ...TeamTableResponseEfficiency\n            ...TeamTableLaunchDate\n            ...TeamTableResolvedReports\n            ...TeamTableMinimumBounty\n            ...TeamTableAverageBounty\n            ...TeamTableAvatarAndTitle\n            __typename\n          }\n          ...InvitationLink\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TeamTableResponseEfficiency on Team {\n  id\n  response_efficiency_percentage\n  ...ResponseEfficiencyIndicator\n  __typename\n}\n\nfragment ResponseEfficiencyIndicator on Team {\n  id\n  response_efficiency_percentage\n  __typename\n}\n\nfragment TeamTableLaunchDate on Team {\n  id\n  launched_at\n  __typename\n}\n\nfragment TeamTableResolvedReports on Team {\n  id\n  resolved_report_count\n  __typename\n}\n\nfragment TeamTableMinimumBounty on Team {\n  id\n  currency\n  base_bounty\n  __typename\n}\n\nfragment TeamTableAverageBounty on Team {\n  id\n  currency\n  average_bounty_lower_amount\n  average_bounty_upper_amount\n  __typename\n}\n\nfragment TeamTableAvatarAndTitle on Team {\n  id\n  profile_picture(size: medium)\n  name\n  handle\n  submission_state\n  triage_active\n  publicly_visible_retesting\n  state\n  allows_bounty_splitting\n  external_program {\n    id\n    __typename\n  }\n  ...TeamLinkWithMiniProfile\n  __typename\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  id\n  handle\n  name\n  __typename\n}\n\nfragment InvitationLink on InvitationInterface {\n  ... on InvitationsSoftLaunch {\n    id\n    token\n    team {\n      id\n      handle\n      submission_requirements {\n        id\n        terms_required_at\n        mfa_required_at\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on InvitationsRetest {\n    id\n    token\n    accepted_at\n    team {\n      id\n      handle\n      submission_requirements {\n        id\n        terms_required_at\n        mfa_required_at\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}
 

    response = requests.post(url=url, json=body,headers=final_header,allow_redirects=False) 

    if response.status_code == 200: 
        data = response.json()

        #Filter the json response

        # Get the list of invitations from "edges" inside "soft_launch_invitations"
        invitations = data["data"]["me"]["soft_launch_invitations"]["edges"]

        #Ask for the REP value you want to decline
        while True:
            try:
                badREF = int(input("Enter the Response Efficiency Percentage you want to decline (downwards/<=): "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        # Filter the invitations based on the response efficiency percentage
        filtered_companies_tokens = [
            (invitation["node"], invitation["node"]["token"])
            for invitation in invitations
            if invitation["node"]["team"]["response_efficiency_percentage"] <= badREF
        ]

        # Check if there are filtered companies to decline
        if filtered_companies_tokens:
            print(f"Declining invitations from companies with response efficiency rate of <= {badREF}%\n")
            
            # Print name and response efficiency rate before declining
            for company, token in filtered_companies_tokens:
                name = company["team"]["name"]
                response_rate = company["team"]["response_efficiency_percentage"]
                
                # Print the extracted values
                print("---------")
                print(f"Company Name: {name}")
                print(f"Response Efficiency Rate: {response_rate}%")
                #print(f"Token: {token}")

                # Send GraphQL request for each token
                decline_request(token, name, final_header)

        else:
            print(f"No invitations found with response efficiency rate of <= {badREF}%.")
    else:
        print(f"Failed to retrieve list of invitations - Status code: {response.status_code}")


def decline_request(token, name, final_header):
 
    url = "https://hackerone.com/graphql"
    body = {"operationName":"RejectInvitation","variables":{"product_area":"team_profile","product_feature":"overview","token": token},"query":"mutation RejectInvitation($token: String!) {\n  rejectInvitation(input: {token: $token}) {\n    was_successful\n    __typename\n  }\n}\n"}

    try:
        response = requests.post(url, json=body, headers=final_header)

        if response.status_code == 200:
            result = response.json()
            if result.get("data", {}).get("rejectInvitation", {}).get("was_successful") == True:
                print(f"Invitation from {name} declined successfully.")
                print("---------")
        else:
            print(f"GraphQL request failed for token {token}. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error while sending GraphQL request for token {token}: {e}")

def main():
    getX_CSRF_TOKEN()


if __name__ == "__main__":
    main()
    