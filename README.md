# HyperRail – Route Optimization & Train Booking System

A web application that finds the optimal route between railway stations using Dijkstra’s shortest path algorithm and allows users to book journeys based on the computed route.

The system models the railway network as a weighted graph, where stations are nodes and routes between stations are edges with distance and cost attributes.
## Deployment link
https://hyperrail.onrender.com/

## Features

Shortest route computation using Dijkstra’s algorithm

Graph representation of a railway network

Route optimization using distance and cost

Interactive route visualization

Ticket booking interface

Flask backend with database integration

## Tech Stack

### Backend

Python

Flask

SQLAlchemy

### Algorithms

Graph data structure

Dijkstra’s shortest path algorithm

### Frontend

HTML

CSS

Jinja templates

### Database

PostgreSQL

## How the Route Optimization Works

The railway network is represented as a graph:

Stations → Nodes

Routes → Edges

Each edge stores:

Distance

Cost

The algorithm minimizes the total weighted route cost:

W = 0.6 × Distance + 0.4 × Cost

Dijkstra’s algorithm is applied to compute the optimal path between the selected source and destination stations.

## Example

For a query:

Mumbai Central → Delhi Central

The algorithm evaluates possible routes such as:

Mumbai → Jaipur → Delhi

Mumbai → Pune → Delhi

Mumbai → Ahmedabad → Jaipur → Delhi

The optimal path selected is:

Mumbai → Jaipur → Delhi
Total Distance: 1300 km
Total Cost: ₹13000

## Running the Project Locally

Clone the repository

git clone https://github.com/yourusername/HyperRail.git
cd HyperRail

Create virtual environment

python -m venv venv
source venv/bin/activate

Install dependencies

pip install -r requirements.txt

Initialize the database

python init_db.py

Run the application

python app.py

Open in browser

http://127.0.0.1:5000
