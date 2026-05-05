package GreenLLM.app.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestBody;


import GreenLLM.app.dto.RequestDashboardResponse;
import GreenLLM.app.dto.RequestModelStatsDto;
import GreenLLM.app.dto.DashboardRequestDto;

import GreenLLM.app.service.RequestDashboardService;


@RestController
@RequestMapping("/api/dashboard")
public class RequestDashboardController {

    private final RequestDashboardService dashboardService;

    public RequestDashboardController(RequestDashboardService dashboardService) {
        this.dashboardService = dashboardService;
    }

    @PostMapping("/stats")
    public ResponseEntity<RequestDashboardResponse> getStats(@RequestBody DashboardRequestDto request) {
        return ResponseEntity.ok(dashboardService.getLlmComparison(request.getQuery()));
    }
}