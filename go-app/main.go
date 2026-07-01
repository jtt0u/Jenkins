package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"runtime"
	"time"
)

var (
	version     = getEnv("APP_VERSION", "dev")
	environment = getEnv("ENVIRONMENT", "development")
	buildTime   = getEnv("BUILD_TIME", time.Now().Format(time.RFC3339))
	gitCommit   = getEnv("GIT_COMMIT", "unknown")
)

type HealthResponse struct {
	Status      string    `json:"status"`
	Version     string    `json:"version"`
	Environment string    `json:"environment"`
	Uptime      string    `json:"uptime"`
	Timestamp   time.Time `json:"timestamp"`
}

type InfoResponse struct {
	Application string            `json:"application"`
	Version     string            `json:"version"`
	Environment string            `json:"environment"`
	BuildTime   string            `json:"build_time"`
	GitCommit   string            `json:"git_commit"`
	GoVersion   string            `json:"go_version"`
	OS          string            `json:"os"`
	Arch        string            `json:"arch"`
	Metadata    map[string]string `json:"metadata,omitempty"`
}

type MetricsResponse struct {
	NumGoroutines int               `json:"num_goroutines"`
	MemoryMB      float64           `json:"memory_mb"`
	GoVersion     string            `json:"go_version"`
	Counters      map[string]int    `json:"counters"`
	CustomMetrics map[string]string `json:"custom_metrics,omitempty"`
}

var (
	startTime      = time.Now()
	requestCounter = make(map[string]int)
)

func main() {
	port := getEnv("PORT", "8080")

	http.HandleFunc("/", handleHome)
	http.HandleFunc("/health", handleHealth)
	http.HandleFunc("/info", handleInfo)
	http.HandleFunc("/metrics", handleMetrics)
	http.HandleFunc("/api/data", handleData)

	log.Printf("Starting server on port %s", port)
	log.Printf("Version: %s, Environment: %s", version, environment)
	log.Printf("Build Time: %s, Commit: %s", buildTime, gitCommit)

	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatal(err)
	}
}

func handleHome(w http.ResponseWriter, r *http.Request) {
	requestCounter["/"]++
	w.Header().Set("Content-Type", "text/html")
	html := fmt.Sprintf(`
<!DOCTYPE html>
<html>
<head>
    <title>Go Application - %s</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #00ADD8; }
        .info { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .endpoint { background: #e8f4f8; padding: 10px; margin: 5px 0; border-left: 3px solid #00ADD8; }
        code { background: #f5f5f5; padding: 2px 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Go Application</h1>
    <div class="info">
        <strong>Version:</strong> %s<br>
        <strong>Environment:</strong> %s<br>
        <strong>Build Time:</strong> %s<br>
        <strong>Git Commit:</strong> %s<br>
        <strong>Go Version:</strong> %s
    </div>
    <h2>Available Endpoints:</h2>
    <div class="endpoint"><code>GET /</code> - This page</div>
    <div class="endpoint"><code>GET /health</code> - Health check endpoint</div>
    <div class="endpoint"><code>GET /info</code> - Application information</div>
    <div class="endpoint"><code>GET /metrics</code> - Application metrics</div>
    <div class="endpoint"><code>GET /api/data</code> - Sample API endpoint</div>
</body>
</html>
`, version, version, environment, buildTime, gitCommit, runtime.Version())
	fmt.Fprint(w, html)
}

func handleHealth(w http.ResponseWriter, r *http.Request) {
	requestCounter["/health"]++
	response := HealthResponse{
		Status:      "healthy",
		Version:     version,
		Environment: environment,
		Uptime:      time.Since(startTime).String(),
		Timestamp:   time.Now(),
	}
	jsonResponse(w, response)
}

func handleInfo(w http.ResponseWriter, r *http.Request) {
	requestCounter["/info"]++

	metadata := make(map[string]string)
	if metaKeys := os.Getenv("METADATA_KEYS"); metaKeys != "" {
		// Example: METADATA_KEYS=key1,key2,key3
		// Will read METADATA_KEY1, METADATA_KEY2, METADATA_KEY3
		for i := 1; i <= 5; i++ {
			key := fmt.Sprintf("METADATA_KEY%d", i)
			if val := os.Getenv(key); val != "" {
				metadata[key] = val
			}
		}
	}

	response := InfoResponse{
		Application: "go-app",
		Version:     version,
		Environment: environment,
		BuildTime:   buildTime,
		GitCommit:   gitCommit,
		GoVersion:   runtime.Version(),
		OS:          runtime.GOOS,
		Arch:        runtime.GOARCH,
		Metadata:    metadata,
	}
	jsonResponse(w, response)
}

func handleMetrics(w http.ResponseWriter, r *http.Request) {
	requestCounter["/metrics"]++

	var m runtime.MemStats
	runtime.ReadMemStats(&m)

	customMetrics := make(map[string]string)
	if metricsEnabled := os.Getenv("CUSTOM_METRICS"); metricsEnabled == "true" {
		customMetrics["uptime_seconds"] = fmt.Sprintf("%.0f", time.Since(startTime).Seconds())
		customMetrics["build_number"] = getEnv("BUILD_NUMBER", "N/A")
	}

	response := MetricsResponse{
		NumGoroutines: runtime.NumGoroutine(),
		MemoryMB:      float64(m.Alloc) / 1024 / 1024,
		GoVersion:     runtime.Version(),
		Counters:      requestCounter,
		CustomMetrics: customMetrics,
	}
	jsonResponse(w, response)
}

func handleData(w http.ResponseWriter, r *http.Request) {
	requestCounter["/api/data"]++

	data := map[string]interface{}{
		"message":     "Hello from Go API",
		"timestamp":   time.Now(),
		"environment": environment,
		"version":     version,
		"items": []map[string]string{
			{"id": "1", "name": "Item One", "status": "active"},
			{"id": "2", "name": "Item Two", "status": "active"},
			{"id": "3", "name": "Item Three", "status": "inactive"},
		},
	}
	jsonResponse(w, data)
}

func jsonResponse(w http.ResponseWriter, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(data)
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
