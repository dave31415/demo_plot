#deploy a flask app with apache on ec2
import sys

apache_dir="/var/www"

def deploy(repo_name,app_name=None):
    '''
       repo_name is what the repo is called on githib
       app_name is the name of the python file file (without the .py)
       assumes the app variable in that file is called "app"
       that is, you will have a line in there like 'app = Flask(__name__)' 
    '''
    if name == None:
        #might be a different name
        name=repo_name 
    repo_dir=apache_dir+'/'+repo_name
    wsgi_file=repo_dir+'/'+app_name
    sites_dir="/etc/apache2/sites-available"
    site_name=app_name
    site_file=sites_dir+'/'+site_name+'.conf'
    
    wsgi_text="import sys \nsys.path.insert(0, '%s') \n\nfrom %s import %s as application" % (repo_dir, app_name)

    fp=open(wsgi_file,'w')
    fp.write(wsgi_text)
    fp.close()
    
    sites_text="""
<VirtualHost *:80>
    WSGIDaemonProcess %s
    WSGIScriptAlias / %s

     <Directory %s>
        WSGIProcessGroup %s
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
     </Directory>
</VirtualHost>
    """ % (app_name,wsgi_file,repo_dir,app_name)
    
if __name__ == "__main__":
    nargs=len(sys.argv)
    if nargs > 3 or nargs <2:
        print "-syntax deploy <repo_name> [app_name]" 
        exit(1)
    repo_name=sys.argv[1]
    if nargs == 3:
        app_name=sys.argv[2]
    else :
        app_name=repo_name
    deploy(repo_name,app_name=app_name)  
    