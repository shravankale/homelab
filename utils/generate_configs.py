"""This is a script to generate configuration files from their templates. This can be useful for version-control of config files such as yaml files without uploading secrets such as passwords or API keys

Usage: Check "python generate_configs.py --help """

import os, re
import yaml, argparse

def generate_configs_from_templates(template_dir, config_dir, env_file):
    
    #Get Secrets
    secrets = {}
    if os.path.isfile(env_file):
        if env_file.split('.')!='env':
            print(f"The {{env_file}} is not a .env environment file")
        with open(env_file, 'r') as file:
            for line in file:
                key,value = line.strip().split('=')
                secrets[key]=value
    elif os.path.isdir(env_file):
        for file in os.listdir(env_file):
            if file.split('.')[-1]=='env':
                with open(os.path.join(env_file,file), 'r') as file:
                    for line in file:
                        key,value = line.strip().split('=')
                        secrets[key]=value
    else:
        if not os.path.exists(env_file):
            print(f"Path {{env_file}}: does not exist")
        else:
            print(f"Path {{env_file}}: exists but is not a directory or file")

    if len(secrets)==0:
        print("No environment files found")
    
    #Using a regex for identifying env vars or secrets in template files
    regex = re.compile(r'{{\s*([\w_]+)\s*}}|\$\{\s*([\w_]+)\s*}')
    
    #Go through template files and generate config files
    for file in os.listdir(template_dir):

        if file.split('.')[-2]=='template':
            template_path = os.path.join(template_dir,file)

            # Extract the base filename without the last extension
            config_filename = file.split('.')[0]+'.yaml'
            config_path = os.path.join(config_dir, config_filename)

            #Replace placeholders with values from secrets
            modified_config = []
            with open(template_path,'r') as template_file: #, open(config_path,'w') as config_file:
                for line in template_file:
                    match = regex.search(line)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--from-templates', action="store_true", help="Generate configs from templates")
    parser.add_argument('--template-dir', type=str, help="Path to templates directory with *.yaml.template files")
    parser.add_argument('--config-dir', type=str, help="Path to output configuration directory for a given service")
    parser.add_argument('--using-env',type=str, help="Path to a secrets environment file")

    args = parser.parse_args()

    if args.from_templates:
        generate_configs_from_templates(args.template_dir, args.config_dir, args.using_env)