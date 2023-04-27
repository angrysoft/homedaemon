package ovh.angrysoft.homedaemon.automation;

import java.util.ArrayList;
import java.util.List;

import com.google.gson.internal.LazilyParsedNumber;

import ovh.angrysoft.homedaemon.automation.actions.Action;
import ovh.angrysoft.homedaemon.automation.actions.ActionDispatch;
import ovh.angrysoft.homedaemon.automation.actions.ActionExecute;
import ovh.angrysoft.homedaemon.automation.actions.ActionState;
import ovh.angrysoft.homedaemon.automation.conditions.AndCondition;
import ovh.angrysoft.homedaemon.automation.conditions.Condition;
import ovh.angrysoft.homedaemon.automation.conditions.IntEqTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.IntGtTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.IntLtTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.NotCondition;
import ovh.angrysoft.homedaemon.automation.conditions.NullTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.OrCondition;
import ovh.angrysoft.homedaemon.automation.conditions.StatusTestCase;
import ovh.angrysoft.homedaemon.automation.conditions.TestCase;
import ovh.angrysoft.homedaemon.devices.DeviceAttribute;
import ovh.angrysoft.homedaemon.devices.DeviceManager;
import ovh.angrysoft.homedaemon.devices.software.StateDevice;

public class AutomationParser {
    private DeviceManager deviceManager;

    public AutomationParser(DeviceManager deviceManager) {
        this.deviceManager = deviceManager;
    }

    public Automation parse(AutomationInfo info) {
        List<Action> actions = this.parseActions(info.getActions());
        List<Action> actionsFalse = this.parseActions(info.getActionsFalse());
        List<Condition> conditions = this.parseConditions(info.getConditions());
        registerStateAttribute(info.getState());
        // TODO: throw parse error if something go wrong
        return new Automation(info.getSid(), conditions, actions, actionsFalse);
    }

    private void registerStateAttribute(List<State> states) {
        if (states == null)
            return;

        StateDevice stateDevice = (StateDevice) deviceManager.getDevice("state");
        states.forEach((state) -> {
            System.out.println("registering (" + state.attrType + "): " + state.attrName + "=" + state.attrValue);
            switch (state.attrType) {
                case "bool":
                    stateDevice.registerStateAttribute(
                            new DeviceAttribute<Boolean>(state.attrName, (Boolean) state.attrValue));
                    break;
                case "str":
                    stateDevice.registerStateAttribute(
                            new DeviceAttribute<String>(state.attrName, (String) state.attrValue));
                    break;
                case "int":
                    stateDevice.registerStateAttribute(
                            new DeviceAttribute<Integer>(state.attrName, (Integer) state.attrValue));
                    break;
            }
        });
    }

    private List<Condition> parseConditions(List<ConditionInfo> conditionsInfos) {
        List<Condition> result = new ArrayList<>();
        for (ConditionInfo conditionInfo : conditionsInfos) {
            Condition condition = null;

            switch (conditionInfo.type) {
                case "and":
                    condition = new AndCondition(deviceManager);
                    break;
                case "or":
                    condition = new OrCondition(deviceManager);
                    break;
                case "not":
                    condition = new NotCondition(deviceManager);
                    break;
            }

            if (condition != null) {
                for (TestCaseInfo testCaseInfo : conditionInfo.testCases) {
                    condition.addCase(this.parseTestCase(testCaseInfo));
                }
                result.add(condition);
            }
        }
        return result;
    }

    private TestCase<?> parseTestCase(TestCaseInfo testCaseInfo) {
        switch (testCaseInfo.type) {
            case "gt": {
                LazilyParsedNumber number = (LazilyParsedNumber) testCaseInfo.attrValue;
                return new IntGtTestCase(testCaseInfo.type, testCaseInfo.sid, testCaseInfo.attrName,
                        number.intValue());
            }
            case "lt": {
                LazilyParsedNumber number = (LazilyParsedNumber) testCaseInfo.attrValue;
                return new IntLtTestCase(testCaseInfo.type, testCaseInfo.sid, testCaseInfo.attrName,
                        number.intValue());
            }
            case "eq": {
                LazilyParsedNumber number = (LazilyParsedNumber) testCaseInfo.attrValue;
                return new IntEqTestCase(testCaseInfo.type, testCaseInfo.sid, testCaseInfo.attrName,
                        number.intValue());
            }
            case "status": {
                return new StatusTestCase(testCaseInfo.type, testCaseInfo.sid, testCaseInfo.attrName,
                        testCaseInfo.attrValue);
            }
            case "state": {
                return new StatusTestCase(testCaseInfo.type, "state", testCaseInfo.attrName,
                        testCaseInfo.attrValue);
            }
            default:
                return new NullTestCase(testCaseInfo.type, testCaseInfo.sid, testCaseInfo.attrName,
                        testCaseInfo.attrValue);
        }
    }

    private List<Action> parseActions(List<ActionInfo> actions) {
        List<Action> result = new ArrayList<>();
        for (ActionInfo actionInfo : actions) {
            result.add(this.parseAction(actionInfo));
        }
        return result;
    }

    private Action parseAction(ActionInfo action) {
        switch (action.getType()) {
            case "execute":
                return new ActionExecute(action.getSid(), action.getCmd(), action.getArg(), action.isRunInBackground(),
                        deviceManager);
            case "dispatch":
                return new ActionDispatch(action.getCmd(), action.getArg(), deviceManager.getBus());
            case "state":
                return new ActionState(action.getCmd(), action.getArg(), deviceManager);
        }
        return null;
    }
}
