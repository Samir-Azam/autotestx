#pragma once

#include <functional>
#include <string>
#include <vector>

struct TestResult {
    std::string name;
    bool passed;
    std::string message;
    double executionTimeMs;
};

struct TestCase {
    std::string name;
    std::function<void()> function;
};

class TestRunner {
public:
    static TestRunner& instance();

    void addTest(
        const std::string& name,
        std::function<void()> function
    );

    int run();

    const std::vector<TestResult>& getResults() const;

private:
    TestRunner() = default;

    std::vector<TestCase> tests;
    std::vector<TestResult> results;

    int passedTests = 0;
    int failedTests = 0;
};

void assertEqual(
    int actual,
    int expected,
    const std::string& expression
);

class TestRegistrar {
public:
    TestRegistrar(
        const std::string& name,
        std::function<void()> function
    );
};

#define AUTOTESTX_CONCAT_IMPL(a, b) a##b
#define AUTOTESTX_CONCAT(a, b) AUTOTESTX_CONCAT_IMPL(a, b)

#define TEST(name) \
    void AUTOTESTX_CONCAT(test_, __LINE__)(); \
    TestRegistrar AUTOTESTX_CONCAT(registrar_, __LINE__)( \
        name, \
        AUTOTESTX_CONCAT(test_, __LINE__) \
    ); \
    void AUTOTESTX_CONCAT(test_, __LINE__)()

#define ASSERT_EQ(actual, expected) \
    assertEqual(actual, expected, #actual)