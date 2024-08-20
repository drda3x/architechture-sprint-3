# Задача 1.1. Анализ текущего приложения и планирование

## Анализ текущего приложения
#### Язык программирования
Java
#### База данных
PostgreSQL
#### Архитектура
Монолитное, однопоточное приложение, принимающее запросы от пользователей и отправляющее запросы к сенсорам.
#### Взаимодействие
Синхронное
#### Масштабируемость
Масштабируемость возможна путем запуска еще одного инстанса приложения целиком
#### Развертывание
Для развертывания нужна установка приложения + установка и настройка БД.

## Домены и границы контекстов
- Домен. Управление устройствами отопления
    - Контекст. Прием управляющих команд от пользователя
    - Контекст. Установка параметров сенсора. Получение данных от сенсора

## План перехода на микросервисную архитектуру
1. Переработка доменов, определение новых контекстов
1. Определение конкретных микросервисов и их описание
1. Определение механизма взаимодействия микросервисов с пользователем
1. Определение механизма взаимодействия микросервисов между собой
1. Подбор стека
1. Выпуск MVP (реализация компонентов, подготовка документации для API)


# Задача 1.2. Декомпозиция приложения на микросервисы
## Домены и границы контекстов
- Домен. Управление устройствами
    - Поддомен. Управление устройствами
        - Контекст. Добавление/Удаление устройств
        - Контекст. Отправка команд устройствам


# Базовая настройка

## Запуск minikube

[Инструкция по установке](https://minikube.sigs.k8s.io/docs/start/)

```bash
minikube start
```


## Добавление токена авторизации GitHub

[Получение токена](https://github.com/settings/tokens/new)

```bash
kubectl create secret docker-registry ghcr --docker-server=https://ghcr.io --docker-username=<github_username> --docker-password=<github_token> -n default
```


## Установка API GW kusk

[Install Kusk CLI](https://docs.kusk.io/getting-started/install-kusk-cli)

```bash
kusk cluster install
```


## Настройка terraform

[Установите Terraform](https://yandex.cloud/ru/docs/tutorials/infrastructure-management/terraform-quickstart#install-terraform)


Создайте файл ~/.terraformrc

```hcl
provider_installation {
  network_mirror {
    url = "https://terraform-mirror.yandexcloud.net/"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
}
```

## Применяем terraform конфигурацию 

```bash
cd terraform
terraform apply
```

## Настройка API GW

```bash
kusk deploy -i api.yaml
```

## Проверяем работоспособность

```bash
kubectl port-forward svc/kusk-gateway-envoy-fleet -n kusk-system 8080:80
curl localhost:8080/hello
```


## Delete minikube

```bash
minikube delete
```
