# 1) Frontend builder
#FROM node:alpine AS frontend-builder
#
#WORKDIR /editor
#
#COPY editor/frontend/package*.json ./
#RUN npm install
#COPY editor/frontend/ ./
#RUN npm run build

# 2) Final runtime
FROM python:3.10-alpine
WORKDIR /app

# Create non-root users
RUN addgroup -S challenger && adduser -S challenger -G challenger \
    && addgroup -S editor \
    && adduser -S editor -G editor -s /bin/bash && addgroup editor challenger

# Add password for root
RUN echo "root:HIDDEN_SORRY_NOT_SORRY" | chpasswd && chmod ug+s /bin/su

# Install dependencies
RUN apk add --no-cache nginx supervisor openjdk11-jre maven bash
#RUN pip install --no-cache-dir flask requests

# Copy the main application
RUN mkdir -p /app/java && chown -R editor:challenger /app/java
COPY challenge/application/pom.xml  ./java/pom.xml
COPY challenge/application/src      ./java/src
WORKDIR /app/java

RUN su editor -c "mvn clean package -DskipTests"
RUN cp target/*.jar app.jar
WORKDIR /app

# Copy files from builders
# COPY editor/backend/ ./backend
#COPY --from=frontend-builder /editor/dist       ./backend/static

# Set permissions
RUN chown -R editor:challenger /app/java
#RUN chown -R editor:editor      /app/backend


# Fix permissions (no cheeky SSTI)
RUN chmod -R 404 /app/java/src/main/resources/application.properties /app/java/pom.xml
RUN chmod -R 555 /app/java/src/main/resources/templates
RUN chmod -R 740 /app/java/src/main/java && chmod -R 770 /app/java/src/main/resources/static /app/java/src/main/resources/packages
#RUN chmod -R 770 /app/backend

# Configure the application
RUN mkdir -p /etc/supervisor.d
COPY config/supervisord.conf  /etc/supervisor.d/supervisord.ini
RUN chmod 660 /etc/supervisord.conf

COPY config/nginx.conf       /etc/nginx/nginx.conf
RUN chown -R root:editor /etc/supervisord.conf && chmod 660 /etc/supervisord.conf
COPY config/proxy_params    /etc/nginx/proxy_params
COPY config/no-exec.policy /opt/no-exec.policy

COPY flag.txt                /flag.txt

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 1337
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]