(function(){
  var app = angular.module('autorunModule', []);

  app.config(function(){

  });

  app.controller('MasterCtrl', function($scope, $http){
    $scope.defaultText = "请在右侧菜单中选择查看项"

    try{
      $scope.outputs = {
        "logon": logon,
        "services": services,
        "internetExplorer": internetExplorer,
        "drivers": drivers,
        "scheduledTasks": scheduledTasks,
        "bootExecute": bootExecute,
        "knownDlls": knownDlls,
        "winsocket": winsocket,
        "winLogon": winLogon,
        "imageHijacks": imageHijacks
      };
    }catch(err){
      $scope.defaultText = "请先运行py脚本生成输出文件";
    }
      

    $scope.tab = "";
    $scope.tabData = "";

    $scope.changeTab = function(tab){
      $scope.tab = tab;
      $scope.tabData = $scope.outputs[tab];
    };
  });

})();
