pipeline {
    agent { label 'dragon' }
    stages {
        stage('setup') {
            steps {
                sh """#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                """
            }
        }
        stage('test - coverage') {
            steps {
                sh """#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    python -m pip install --upgrade coverage pytest
                    python -m coverage run --branch --source wmc -m pytest --disable-pytest-warnings --junitxml junittest-coverage.xml
                    python -m coverage xml
                """
            }
        }
        stage('test - pylint') {
            steps {
                sh """#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    python -m pip install pylint pylint_junit
                    python -m pylint --rcfile=setup.cfg --output-format=pylint_junit.JUnitReporter wmc | tee junittest-pylint.xml
                """
            }
        }
        stage('build') {
            steps {
                sh """#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    python -m pip install --upgrade wheel setuptools
                    python setup.py sdist bdist_wheel
                """
            }
        }
    }
    post {
        always {
            junit allowEmptyResults: true, healthScaleFactor: 0.0, testResults: 'junittest*.xml'
            step([$class: 'CoberturaPublisher', autoUpdateHealth: false, autoUpdateStability: false, coberturaReportFile: 'coverage.xml', failUnhealthy: false, failUnstable: false, maxNumberOfBuilds: 0, onlyStable: false, sourceEncoding: 'ASCII', zoomCoverageChart: false])
        }
        cleanup {
            cleanWs()
        }
    }
}
