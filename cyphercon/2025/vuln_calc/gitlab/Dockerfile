FROM gitlab/gitlab-ce:latest

# Set environment variables for GitLab
ENV GITLAB_OMNIBUS_CONFIG="external_url 'http://localhost/'; gitlab_rails['initial_root_password'] = 'omgwtfbbq';"

# Expose GitLab ports
EXPOSE 80 443 22

# The container will automatically start GitLab 