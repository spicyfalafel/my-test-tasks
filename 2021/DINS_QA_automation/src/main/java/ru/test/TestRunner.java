package ru.test;

import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

/*
    I confess I couldn't create the jar properly using maven so I
    copied tests here...
 */

public class TestRunner {
    public static void main(String[] args) {
        Result result = JUnitCore.runClasses(RestTest.class);

        for (Failure failure : result.getFailures()) {
            System.out.println("---------------");
            System.out.println(failure.toString());
        }

        System.out.println("All tests were successful: " + result.wasSuccessful());
    }
}  