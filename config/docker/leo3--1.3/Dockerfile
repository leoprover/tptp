FROM openjdk:8-alpine
RUN apk update \                                              
 && apk add ca-certificates wget \                                     
 && update-ca-certificates
RUN wget -P /usr/src/leo3 https://github.com/leoprover/Leo-III/releases/download/v1.3/leo3.jar
WORKDIR /usr/src/leo3
ENTRYPOINT ["java", "-jar", "leo3.jar"]
