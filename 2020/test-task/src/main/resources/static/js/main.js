let helloWorldTestApp = angular.module("helloWorldTestApp", []);


helloWorldTestApp.controller("HelloWorldCtrl", ['$scope', '$http', function ($scope, $http) {
    $scope.getUsers = function () {
        console.log("getting users...")
        $http({
            method: 'GET',
            url: '/api/v1/user/',
            headers: {'Content-Type': 'application/json'},
        }).then(function succ(response) {
            $scope.allUsers = response.data
        }, function bad(error) {
            console.log("error:")
            console.log(error)
        })
    }
    $scope.getUsers()

    $scope.currentOrders = []

    $scope.showOrders = function(orders){
        $scope.currentOrders = orders
        $('#orders-modal').modal('show');
    }
}])