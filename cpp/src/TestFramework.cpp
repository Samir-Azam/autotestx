#include "TestFramework.h"

#include <chrono>
#include <iostream>
#include <stdexcept>
#include <fstream>

TestRunner& TestRunner::instance() {
    static TestRunner runner;
    return runner;
}

void TestRunner::addTest(
    const std::string& name,
    std::function<void()> function
) {
    tests.push_back({name, function});
}

const std::vector<TestResult>& TestRunner::getResults() const {
    return results;
}

int TestRunner::run() {

    results.clear();
    passedTests = 0;
    failedTests = 0;

    std::cout << "\n";
    std::cout << "================================\n";
    std::cout << "           AutoTestX             \n";
    std::cout << "================================\n\n";

    for (const auto& test : tests) {

        auto start = std::chrono::high_resolution_clock::now();

        TestResult result;
        result.name = test.name;

        try {

            test.function();

            auto end = std::chrono::high_resolution_clock::now();

            result.passed = true;
            result.message = "Test passed";

            result.executionTimeMs =
                std::chrono::duration<double, std::milli>(
                    end - start
                ).count();

            std::cout << "[PASS] "
                      << result.name
                      << " ("
                      << result.executionTimeMs
                      << " ms)\n";

            passedTests++;

        } catch (const std::exception& error) {

            auto end = std::chrono::high_resolution_clock::now();

            result.passed = false;
            result.message = error.what();

            result.executionTimeMs =
                std::chrono::duration<double, std::milli>(
                    end - start
                ).count();

            std::cout << "[FAIL] "
                      << result.name
                      << " ("
                      << result.executionTimeMs
                      << " ms)"
                      << " -> "
                      << result.message
                      << "\n";

            failedTests++;
        }

        results.push_back(result);
    }

    std::cout << "\n--------------------------------\n";
    std::cout << "Total:  " << tests.size() << "\n";
    std::cout << "Passed: " << passedTests << "\n";
    std::cout << "Failed: " << failedTests << "\n";
    std::cout << "--------------------------------\n";

    return failedTests;
}

void assertEqual(
    int actual,
    int expected,
    const std::string& expression
) {

    if (actual != expected) {

        throw std::runtime_error(
            expression +
            " | Expected: " +
            std::to_string(expected) +
            " | Actual: " +
            std::to_string(actual)
        );
    }
}

TestRegistrar::TestRegistrar(
    const std::string& name,
    std::function<void()> function
) {
    TestRunner::instance().addTest(name, function);
}

void TestRunner::writeJsonReport(const std::string& filename) const {

    std::ofstream file(filename);

    if (!file.is_open()) {
        throw std::runtime_error(
            "Unable to create JSON report: " + filename
        );
    }

    file << "{\n";

    file << "  \"summary\": {\n";
    file << "    \"total\": " << tests.size() << ",\n";
    file << "    \"passed\": " << passedTests << ",\n";
    file << "    \"failed\": " << failedTests << "\n";
    file << "  },\n";

    file << "  \"tests\": [\n";

    for (size_t i = 0; i < results.size(); ++i) {

        const auto& result = results[i];

        file << "    {\n";

        file << "      \"name\": \""
             << result.name
             << "\",\n";

        file << "      \"passed\": "
             << (result.passed ? "true" : "false")
             << ",\n";

        file << "      \"message\": \""
             << result.message
             << "\",\n";

        file << "      \"execution_time_ms\": "
             << result.executionTimeMs
             << "\n";

        file << "    }";

        if (i + 1 < results.size()) {
            file << ",";
        }

        file << "\n";
    }

    file << "  ]\n";
    file << "}\n";

    file.close();
}