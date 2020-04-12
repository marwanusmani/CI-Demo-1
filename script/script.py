import os

#import script
importFile = '../import/_import.py'
importFileResult = 'import.txt'

#GitDeployment script
gitDeploymentFile = '../GithubDeployment/_githubDeployment.py'
gitDeploymentResult = 'gitDeployment.txt'

#packagePublishing script
packagePublishing = '../PackagePublishing/_publishPackages.py'
packagePublishingResult = 'packagePublish.txt'

#portal scripts
updatePortalSettings = '../UpdatePortal/_updatePortalSettings.py'
updatePortal = '../UpdatePortal/_updatePortal.py'
updatePortalResults = 'portal.txt'

# run import script
try:
    os.system("python " + importFile)
    if(os.stat(importFileResult).st_size == 0):
        print("import successfull")
        os.system("python " + gitDeploymentFile + " java_eclipse_jre_lib")
        if(os.stat(gitDeploymentResult).st_size == 0):
            print("Github Deployment for java successfull")
            os.system("python " + gitDeploymentFile + " angular_javascript_lib")
            if(os.stat(gitDeploymentResult).st_size == 0):
                print("Github Deployment for Angular successfull")
                os.system("python " + packagePublishing)
                if(os.stat(packagePublishingResult).st_size == 0):
                    print("Package Deployment for Python Successfull")
                    os.system("python " + updatePortalSettings)
                    if(os.stat(updatePortalResults).st_size == 0):
                        print("Portal Settings Updated Successfully")
                        os.system("python " + updatePortal)
                        if(os.stat(updatePortalResults).st_size == 0):
                            print("Portal Updated Successfully")
                        else:
                            print("portal FAILED to update!")
                            raise ValueError('portal FAILED to update!')
                    else:
                        print("Portal Settings FAILED to updated")
                        raise ValueError('Portal Settings FAILED to updated')
                else:
                    print("Package Deployment for Python FAILED!")
                    raise ValueError('Package Deployment for Python FAILED!')
            else:
                print("Github Deployment for Angular FAILED!")
                raise ValueError('Github Deployment for Angular FAILED!')  
        else:
            print("Github Deployment for Java FAILED!")
            raise ValueError('Github Deployment for Java FAILED!')
    else:
        print("import failed")
        raise ValueError('import failed')
except (ValueError, IndexError):
    exit('Could not complete request.')



