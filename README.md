<h1 id="ai-powered-question-answering-application">🏡AI-Powered Question Answering Application</h1>

<h2 id="table-of-contents">📙<strong>Table of Contents</strong></h2>
<ul>
    <li><a href="#ai-powered-question-answering-application"><strong>🏡AI-Powered Question Answering Application</strong></a></li>
    <li><a href="#table-of-contents">📙<strong>Table of Contents</strong></a>
        <ul>
            <li><a href="#description">🏡<strong>Description</strong></a></li>
            <li><a href="#features">📗<strong>Features</strong></a></li>
            <li><a href="#installation">📦<strong>Installation</strong></a>
                <ul>
                    <li><a href="#prerequisites">Prerequisites</a></li>
                    <li><a href="#setup">Setup</a></li>
                </ul>
            </li>
            <li><a href="#api-documentation">📚<strong>API Documentation</strong></a>
                <ul>
                    <li><a href="#endpoint-answer">Endpoint: <code>/predict</code></a>
                        <ul>
                            <li><a href="#request">Request</a></li>
                            <li><a href="#response">Response</a></li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li><a href="#cicd-pipeline">🔄<strong>CI/CD Pipeline</strong></a>
                <ul>
                    <li><a href="#pipeline-trigger">Pipeline Trigger</a></li>
                </ul>
            </li>
            <li><a href="#running-tests">🧪<strong>Running Tests</strong></a></li>
            <li><a href="#deployment">🚀<strong>Deployment</strong></a>
                <ul>
                    <li><a href="#docker-build-and-push">Docker Build and Push</a></li>
                    <li><a href="#ecs-deployment">ECS Deployment</a></li>
                </ul>
            </li>
            <li><a href="#metrics-and-logging">📊<strong>Metrics and Logging</strong></a></li>
        </ul>
    </li>
</ul>

<hr>

<h2 id="description">🏡<strong>Description</strong></h2>
<p>This repository contains a Python application that provides an AI-powered question-answering service using <strong>Anthropic Claude 3 Haiku</strong> via <strong>AWS Bedrock</strong>. The application is built with <strong>FastAPI</strong> and implements best practices, such as error handling, structured logging, and performance tracking.</p>

<p>The repository includes a fully automated CI/CD pipeline that ensures code quality, builds and pushes a <strong>Docker image</strong>, and deploys the application to <strong>AWS ECS</strong>.</p>

<p>💡If you want to try it out the deployed version, execute the following command</p>
<pre><code>curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"question": "Where is the capital of France?"}' \
     http://app-alb-1578298349.eu-west-2.elb.amazonaws.com/predict
</code></pre>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>

<hr>

<h2 id="features">📗<strong>Features</strong></h2>
<ul>
    <li><strong>FastAPI Endpoint</strong>: A REST API endpoint to accept questions and return AI-generated answers.</li>
    <li><strong>AWS Bedrock Integration</strong>: Connects to <strong>Anthropic Claude 3 Haiku</strong> for LLM-based answers.</li>
    <li><strong>Error Handling</strong>: Robust validation and graceful handling of errors.</li>
    <li><strong>Performance Metrics</strong>: Tracks LLM response times for performance monitoring.</li>
    <li><strong>CI/CD Pipeline</strong>:
        <ul>
            <li>Runs tests with <code>pytest</code> and generates a coverage report.</li>
            <li>Lints and formats code using <code>pylint</code> and <code>black</code>.</li>
            <li>Builds a <code>Docker image</code> and pushes it to <code>AWS ECR</code>.</li>
            <li>Deploys the application to <code>ECS</code> with updated task definitions.</li>
        </ul>
    </li>
</ul>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>

<hr>

<h2 id="installation">📦<strong>Installation</strong></h2>

<h3 id="prerequisites">Prerequisites</h3>
<ul>
    <li><strong>Python 3.10+</strong></li>
    <li><strong>AWS CLI</strong> configured with required permissions</li>
    <li><strong>Docker</strong> installed and configured</li>
    <li><strong>AWS Bedrock</strong> access credentials</li>
</ul>

<h3 id="setup">Setup</h3>
<ol>
    <li>Clone the repository:
        <pre><code>git clone git@github.com:rcanelav/rs-qa.git
cd rs-qa</code></pre>
    </li>
    <li>Install dependencies:
        <pre><code>make install</code></pre>
    </li>
    <li>Set up environment variables:
        <pre><code>cp template.env .env  #And fill with your values</code></pre>
    </li>
    <li>Run the application:
        <ol>
            <li>Local using development mode:
                <pre><code>make run</code></pre>
            </li>
            <li>Local using Docker:
                <pre><code>make docker-build-and-run</code></pre>
            </li>
        </ol>
    </li>
    <li>There are more commands, if you are interested in knowing more
        <pre><code>make help</code></pre>
    </li>
</ol>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>

<hr>

<h2 id="api-documentation">📚<strong>API Documentation</strong></h2>

<h3 id="endpoint-answer">Endpoint: <code>/predict</code></h3>

<p><strong>Method</strong>: <code>POST</code><br>
<strong>Description</strong>: Accepts a question and returns an AI-generated answer.</p>

<h4 id="request">Request</h4>
<p><strong>Payload</strong>:</p>
<pre><code>{
  "question": "What is the capital of France?"
}
</code></pre>

<h4 id="response">Response</h4>
<p><strong>Success (200)</strong>:</p>
<pre><code>{
  "response": "The capital of France is Paris."
}
</code></pre>
<p><strong>Error (4xx/5xx)</strong>:</p>
<pre><code>{
  "message": "Error message."
}
</code></pre>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>
<hr>

<h2 id="cicd-pipeline">🔄<strong>CI/CD Pipeline</strong></h2>

<p>This repository includes a GitHub Actions pipeline that automates the following:</p>
<ol>
    <li><strong>Testing</strong>: Runs <code>pytest</code> to execute the test suite and generate a coverage report.</li>
    <li><strong>Linting and Formatting</strong>: Ensures code quality using <code>pylint</code> and <code>black</code>.</li>
    <li><strong>Dockerization</strong>: Builds a Docker image and pushes it to <code>AWS Elastic Container Registry (ECR)</code>.</li>
    <li><strong>Deployment</strong>: Updates the <code>AWS ECS</code> service with the new image and deploys it by creating a new task revision.</li>
</ol>

<h3 id="pipeline-trigger">Pipeline Trigger</h3>
<p>The pipeline runs automatically on every push to the <code>main</code> branch or executing a <code>workflow_dispatch</code></p>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>

<hr>

<h2 id="running-tests">🧪<strong>Running Tests</strong></h2>

<ol>
    <li>To run tests:
        <pre><code>make tests</code></pre>
    </li>
</ol>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>
<hr>

<h2 id="deployment">🚀<strong>Build containers</strong></h2>

<h3 id="docker-build-and-push">Docker Build and Push</h3>
<ol>
    <li>Build the Docker image:
        <pre><code>make docker-build</code></pre>
    </li>
    <li>Build the Docker image from scratch:
        <pre><code>make docker-build-no-cache</code></pre>
    </li>
    <li>Run container
        <pre><code>make docker-run</code></pre>
    </li>
</ol>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>

<hr>

<h2 id="ecs-deployment">🚀 <strong>Deployment</strong></h2>

<p>This repository includes an automated deployment pipeline, if you want to explore these steps:</p>
  <ol>
    <li><a href="./.github/workflows/_deploy.yml#L39">🏗️Go to <strong>Containerization</strong> step</a></li>
  <li><a href="./.github/workflows/_deploy.yml#L64">🏗️Go to <strong>Deployment</strong> step</a></li>
  </ol>

<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>

<hr>

<h2 id="metrics-and-logging">📊<strong>Metrics and Logging</strong></h2>

<ul>
    <li><strong>Structured Logs</strong>: Logs are output in JSON format for easy integration with tools like AWS CloudWatch.</li>
    <li><strong>Performance Metrics</strong>: Tracks and logs the LLM response time for performance analysis.</li>
</ul>
<div style="text-align: right;">
  <a href="#table-of-contents">Go to Top</a>
</div>


<hr>
<br>
<i>Thank you for reading. 🚀</i>
