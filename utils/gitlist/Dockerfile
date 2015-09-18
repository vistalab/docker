# Build a docker image that can provide a webUI for a git repo
# using GitList (gitlist.org).
#
# Example usage:
#
# Start the container
# ```
#   docker run -d \
#       -name gitlist
#       -p 80:80 \
#       -v <repos/on/disk>:/repos \
#       vistalab/gitlist
#```
# Stop the container
# ```
#   docker stop gitlist
# ```

FROM ubuntu-debootstrap:trusty
MAINTAINER Michael Perry <lmperry@stanford.edu>

# Install
RUN apt-get update \
    && apt-get install -y php5 apache2 git wget \
    && cd /var/www/ \
    && wget https://s3.amazonaws.com/gitlist/gitlist-0.5.0.tar.gz \
    && tar -xzvf gitlist-0.5.0.tar.gz -C /var/www \
    && rm -rf /var/www/gitlist-0.5.0 /var/www/html \
    && mkdir /var/www/gitlist/cache \
    && chmod -R 777 /var/www/gitlist/cache \
    && echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Copy custom files and configs
COPY config.ini /var/www/gitlist/config.ini
COPY gitlist.conf /etc/apache2/conf-available/gitlist.conf
COPY apache.conf /etc/apache2/sites-enabled/000-default.conf
COPY custom_navigation.twig /var/www/gitlist/themes/default/twig/navigation.twig
COPY custom_footer.twig /var/www/gitlist/themes/default/twig/footer.twig

# Enable config
RUN a2enconf gitlist \
    && a2enmod rewrite \
    && apachectl restart

CMD ["apache2ctl", "-D", "FOREGROUND"]





