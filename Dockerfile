FROM eclipse-temurin:21 AS base

FROM base AS builder
WORKDIR /app
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY src src
RUN ./mvnw clean install -DskipTests
# RUN java -Djarmode=layertools -jar target/homed-web-backend-0.1.0.jar extract

FROM base AS runner
WORKDIR /app
RUN mkdir devices.d
RUN mkdir configs.d
RUN mkdir automations.d
COPY --from=builder target/homedaemon-0.3.4-jar-with-dependecies.jar .
# RUN addgroup --system --gid 666 homed-web
# RUN adduser --system --group --uid 666 homed-web
# USER homed-web
# EXPOSE 8080
ENV VERSION=0.3.4
ENV DEVICE_DIR=/app/devices.d
ENV CONFIG_DIR=/app/configs.d
ENV AUTOMATION_DIR=/app/automations.d
ENTRYPOINT ["java", "-jar", "homedaemon-0.3.4-jar-with-dependecies.jar"]