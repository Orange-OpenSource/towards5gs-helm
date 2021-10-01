#
# Software Name : towards5gs-helm
# SPDX-FileCopyrightText: Copyright (c) 2021 Orange
# SPDX-License-Identifier: Apache-2.0
#
# This software is distributed under the Apache License 2.0,
# the text of which is available at https://github.com/Orange-OpenSource/towards5gs-helm/blob/main/LICENSE
# or see the "LICENSE" file for more details.
#
# Author: Abderaouf KHICHANE, Ilhem FAJJARI, Ayoub BOUSSELMI
# Software description: An open-source project providing Helm charts to deploy 5G components (Core + RAN) on top of Kubernetes
#
{{/*
Expand the name of the chart.
*/}}
{{- define "free5gc-n3iwf.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "free5gc-n3iwf.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "free5gc-n3iwf.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "free5gc-n3iwf.labels" -}}
helm.sh/chart: {{ include "free5gc-n3iwf.chart" . }}
{{ include "free5gc-n3iwf.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "free5gc-n3iwf.selectorLabels" -}}
app.kubernetes.io/name: {{ include "free5gc-n3iwf.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
n3iwf Pod Annotations
*/}}
{{- define "free5gc-n3iwf.n3iwfAnnotations" -}}
{{- with .Values.n3iwf }}
{{- if .podAnnotations }}
{{- toYaml .podAnnotations }}
{{- end }}
{{- end }}
{{- end }}

