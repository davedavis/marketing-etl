from auth_helper import *
from customermanagement_example_helper import *

# You must provide credentials in auth.py.

def main(authorization_data):
    
    try:
        output_status_message("-----\nGetUser:")
        get_user_response=customer_service.GetUser(
            UserId=None
        )
        user = get_user_response.User
        customer_roles=get_user_response.CustomerRoles
        output_status_message("CustomerRoles:")
        output_array_of_customerrole(customer_roles)

        # Search for the accounts that the user can access.
        # To retrieve more than 100 accounts, increase the page size up to 1,000.
        # To retrieve more than 1,000 accounts you'll need to add paging.

        accounts=search_accounts_by_user_id(customer_service, user.Id)

        customer_ids=[]
        for account in accounts['AdvertiserAccount']:
            customer_ids.append(account.ParentCustomerId)


    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    customer_service=ServiceClient(
        service='CustomerManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
