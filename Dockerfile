FROM eclipse-temurin:21 AS base
ARG HOMED_VERSION="0.3.4"

FROM maven:eclipse-temurin AS builder
WORKDIR /app
COPY pom.xml .
COPY src src
RUN mvn clean compile assembly:single -DskipTests


FROM base AS runner
WORKDIR /app
RUN mkdir devices.d
RUN mkdir configs.d
RUN mkdir automations.d
COPY --from=builder target/homedaemon-${HOMED_VERSION}-jar-with-dependencies.jar .
# RUN addgroup --system --gid 666 homed-web
# RUN adduser --system --group --uid 666 homed-web
# USER homed-web
# EXPOSE 8080
ENV VERSION=${HOMED_VERSION}
ENV DEVICE_DIR=/app/devices.d
ENV CONFIG_DIR=/app/configs.d
ENV AUTOMATION_DIR=/app/automations.d
ENTRYPOINT ["java", "-jar", "homedaemon-${HOMED_VERSION}-jar-with-dependencies.jar"]