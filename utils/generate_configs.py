"""This is a script to generate configuration files from their templates. This can be useful for version-control of config files such as yaml files without uploading secrets such as passwords or API keys

Usage: Check "python generate_configs.py --help """

import os, re
import yaml, argparse

#Using a regex for identifying env vars or secrets in template files
REGEX = re.compile(r'{{\s*([\w_]+)\s*}}|\$\{\s*([\w_]+)\s*}')

def get_secrets(env):

    secrets = {}
    if os.path.isfile(env):
        if env.split('.')!='env':
            print(f"The {{env}} is not a .env environment file")
        with open(env, 'r') as file:
            for line in file:
                key,value = line.strip().split('=')
                secrets[key]=value
    elif os.path.isdir(env):
        for file in os.listdir(env):
            if file.split('.')[-1]=='env':
                with open(os.path.join(env,file), 'r') as file:
                    for line in file:
                        key,value = line.strip().split('=')
                        secrets[key]=value
    else:
        if not os.path.exists(env):
            print(f"Path {{env}}: does not exist")
        else:
            print(f"Path {{env}}: exists but is not a directory or file")

    if len(secrets)==0:
        print("No environment files found")

    return secrets

def template_to_config(file, file_dir, config_dir,secrets):

    if file.split('.')[-2]=='template':
        template_path = os.path.join(file_dir,file)

        # Extract the base filename without the last extension
        config_filename = file.split('.')[0]+'.yaml'
        config_path = os.path.join(config_dir, config_filename)

        #Replace placeholders with values from secrets
        modified_config = []
        with open(template_path,'r') as template_file: #, open(config_path,'w') as config_file:
            for line in template_file:
                match = REGEX.search(line)
                if match:
                    if match.group(1):
                        key = match.group(1)
                    else:
                        key = match.group(2)
                    #.get(key,default) is useful in case of errors such as missing values
                    line = line.replace(match.group(0), secrets.get(key, match.group(0)))
                    modified_config.append(line)
                else:
                    modified_config.append(line)
            
        with open(config_path,'w') as config_file:
            config_file.writelines(modified_config)

def generate_configs_from_templates(template, config_dir, secrets):
    
    #Go through template files and generate config files
    if os.path.isfile(template):
        file = os.path.basename(template)
        file_dir = os.path.dirname(template)
        template_to_config(file,file_dir,config_dir,secrets)
    elif os.path.isdir(template):
        for file in os.listdir(template):
            template_to_config(file,template,config_dir,secrets)
    else:
        print(f"{template} as a file or directory does not exist")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--from-templates', action="store_true", help="Generate configs from templates")
    parser.add_argument('--template', type=str, help="Path to templates directory with *.template.yaml files or a single file")
    parser.add_argument('--config-dir', type=str, help="Path to output configuration directory for a given service")
    parser.add_argument('--using-env',type=str, help="Path to a secrets environment file or a directory with .env files")

    args = parser.parse_args()

    if args.from_templates:
        #Get Secrets
        secrets = get_secrets(args.using_env)
        generate_configs_from_templates(args.template,args.config_dir, secrets)

# --from-templates --template utils/sample_config.template.yaml --config-dir utils --using-env utils