#include "Calculator.h"
#include "TestFramework.h"
#include <iostream>

Calculator calculator;

TEST("addition") {
    ASSERT_EQ(calculator.add(2, 3), 5);
}

TEST("subtraction") {
    ASSERT_EQ(calculator.subtract(10, 4), 6);
}

TEST("multiplication") {
    ASSERT_EQ(calculator.multiply(3, 4), 12);
}

TEST("failing test") {
    ASSERT_EQ(calculator.add(2, 2), 10);
}

int main() {

    TestRunner& runner = TestRunner::instance();

    int exitCode = runner.run();

    runner.writeJsonReport("results.json");

    std::cout << "\nJSON report generated: results.json\n";

    return exitCode;
}